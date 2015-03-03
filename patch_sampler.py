#!/usr/bin/env python
""" patch_sampler.py
Usage:
  patch_sampler.py  <root_dir>
                    [--samples_per_spectrogram=<samples_per_spectrogram>]
                    [--max_examples_per_file=<max_examples_per_file>]
                    [--verbose]
"""

import os
import numpy as np
import h5py
import cPickle as pkl


class SpectrogramMFCC(object):

    def __init__(self, spec_mat, mfcc_mat, num_samples):
        try:
            with h5py.File(spec_mat, 'r') as f:
                self.spec_mat = f['ps/value'].value
        except Exception as e:
            print 'Error in file', spec_mat
            raise e
        try:
            with h5py.File(mfcc_mat, 'r') as f:
                self.mfcc_mat = f['mfc/value'].value
        except Exception as e:
            print 'Error in file', mfcc_mat
            raise e
        self.num_samples = num_samples

    def sample_patch(self, x_len):

        x_max, y_max = self.spec_mat.shape

        for i in xrange(self.num_samples):
            x_start = np.random.randint(low=0, high=x_max-x_len)

            mfcc_patch = self.mfcc_mat[x_start:x_start+x_len, :]
            spec_patch = self.spec_mat[x_start:x_start+x_len, :]

            assert mfcc_patch.shape == (spec_patch.shape[0], 39)

            yield spec_patch.reshape(1, 1, -1, x_len), mfcc_patch.reshape(1, 1, -1, x_len)


class PatchSampler(object):

    def __init__(self, spec_dir, mfcc_dir, samples_per_spectrogram=10, x_len=100, verbose=False):
        self.spec_dir = spec_dir
        self.mfcc_dir = mfcc_dir
        self.n = samples_per_spectrogram
        self.x_len = x_len
        self.verbose = verbose

    def __iter__(self):
        for root, dirs, files in os.walk(self.mfcc_dir, topdown=False):
            if self.verbose:
                print 'sampling from folder', root

            for name in files:
                if not name.endswith('.hdf5'): continue

                mfcc = os.path.join(root, name)
                spec = mfcc.replace(self.mfcc_dir, self.spec_dir).replace('wav.mfcc', 'wav.spec')
                assert os.path.isfile(mfcc), "mfcc file %s does not exist" % mfcc
                assert os.path.isfile(spec), "spec file %s does not exist" % spec

                pair = SpectrogramMFCC(spec, mfcc, self.n)
                for idx, patches in enumerate(pair.sample_patch(x_len=self.x_len)):
                    yield patches


def write_out(data, label, fname):

    # HDF5 is pretty efficient, but can be further compressed.
    comp_kwargs = {'compression': 'gzip', 'compression_opts': 1}
    with h5py.File(fname, 'w') as f:
        f.create_dataset('data', data=data, **comp_kwargs)
        f.create_dataset('label', data=label, **comp_kwargs)

if __name__ == '__main__':
    from docopt import docopt
    args = docopt(__doc__)

    from pprint import pprint
    print 'User arguments:'
    pprint(args)

    # the number of examples to write to the output hdf5 file before switching to a new one
    if args['--max_examples_per_file']:
        max_examples_per_file = int(args['--max_examples_per_file'])
    else:
        max_examples_per_file = 1000

    # how many times to sample from a given spectrogram
    if args['--samples_per_spectrogram']:
        samples_per_spectrogram = int(args['--samples_per_spectrogram'])
    else:
        samples_per_spectrogram = 5

    # where are the spectrograms
    root = args['<root_dir>']
    spec_dir = os.path.join(root, 'spec')
    mfcc_dir = os.path.join(root, 'mfcc')
    out_dir = os.path.join(root, 'sampled')
    if not os.path.isdir(out_dir): os.makedirs(out_dir)

    def get_fname(filenum):
        return os.path.join(out_dir, 'file.' + str(filenum) + '.h5')

    sampler = PatchSampler(spec_dir, mfcc_dir, samples_per_spectrogram, verbose=True if args['--verbose'] else False)

    patches_sampled = 0; filenum = 0; total_patches_seen = 0
    spec = None; mfcc = None; mfcc_mean = None; spec_mean = None
    for spec_patch, mfcc_patch in sampler:
        patches_sampled += 1

        # update the running means
        mfcc_mean = mfcc_patch.copy() if mfcc_mean is None else (mfcc_mean * total_patches_seen + mfcc_patch) / float(total_patches_seen+1)
        spec_mean = spec_patch.copy() if spec_mean is None else (spec_mean * total_patches_seen + spec_patch) / float(total_patches_seen+1)

        # concatenate the patches to buffer the write
        spec = spec_patch if spec is None else np.concatenate((spec, spec_patch), axis=0)
        mfcc = mfcc_patch if mfcc is None else np.concatenate((mfcc, mfcc_patch), axis=0)

        if patches_sampled == max_examples_per_file:
            print 'writing out files', filenum
            # write a new file
            write_out(spec.astype('float32'), mfcc.astype('float32'), get_fname(filenum))
            filenum += 1
            # empty buffers
            spec = None; mfcc = None; patches_sampled = 0

    # write out book keeping files
    with open(os.path.join(out_dir, 'filelist.txt'), 'wb') as f:
        for i in xrange(filenum):
            f.write(get_fname(i) + '\n')

    # write out accumulated means
    with open(os.path.join(out_dir, 'means.pkl'), 'wb') as f:
        pkl.dump({'mfcc': mfcc_mean, 'spec': spec_mean}, f)
