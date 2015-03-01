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


class SpectrogramPair(object):

    def __init__(self, noisy_mat, clean_mat, num_samples):
        with h5py.File(noisy_mat, 'r') as f:
            self.noisy_mat = f['ps/value'].value
        with h5py.File(clean_mat, 'r') as f:
            self.clean_mat = f['ps/value'].value
        self.num_samples = num_samples

    def sample_patch(self, y_len, x_len):

        y_max, x_max = self.clean_mat.shape

        for i in xrange(self.num_samples):
            y_start = np.random.randint(low=0, high=y_max-y_len)
            x_start = np.random.randint(low=0, high=x_max-x_len)

            clean_patch = self.clean_mat[y_start:y_start+y_len, x_start:x_start+x_len]
            noisy_patch = self.noisy_mat[y_start:y_start+y_len, x_start:x_start+x_len]

            yield noisy_patch.reshape(1, 1, y_len, x_len), clean_patch.reshape(1, 1, y_len, x_len)


class PatchSampler(object):

    def __init__(self, clean_dir, noisy_dir, samples_per_spectrogram=10, x_len=100, y_len=100, verbose=False):
        self.clean_dir = clean_dir
        self.noisy_dir = noisy_dir
        self.n = samples_per_spectrogram
        self.x_len = x_len
        self.y_len = y_len
        self.verbose = verbose

    def __iter__(self):
        for root, dirs, files in os.walk(self.clean_dir, topdown=False):
            if self.verbose:
                print 'sampling from folder', root

            for name in files:
                if not name.endswith('.hdf5'): continue

                clean = os.path.join(root, name)
                noisy = clean.replace(self.clean_dir, self.noisy_dir)
                assert os.path.isfile(clean)
                assert os.path.isfile(noisy)

                pair = SpectrogramPair(noisy, clean, self.n)
                for idx, patches in enumerate(pair.sample_patch(x_len=self.x_len, y_len=self.y_len)):
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
    max_examples_per_file = int(args.get('<max_examples_per_file>', 1000))

    # how many times to sample from a given spectrogram
    samples_per_spectrogram = int(args.get('<samples_per_spectrogram>', 5))

    # where are the spectrograms
    root = args['<root_dir>']
    clean_dir = os.path.join(root, 'clean')
    noisy_dir = os.path.join(root, 'noisy')
    out_dir = os.path.join(root, 'sampled')
    if not os.path.isdir(out_dir): os.makedirs(out_dir)

    def get_fname(filenum):
        return os.path.join(out_dir, 'file.' + str(filenum) + '.h5')

    sampler = PatchSampler(clean_dir, noisy_dir, samples_per_spectrogram, verbose=True if args['--verbose'] else False)

    patches_sampled = 0; filenum = 0; total_patches_seen = 0
    noisy = None; clean = None; clean_mean = None; noisy_mean = None
    for noisy_patch, clean_patch in sampler:
        patches_sampled += 1

        # update the running means
        clean_mean = clean_patch.copy() if clean_mean is None else (clean_mean * total_patches_seen + clean_patch) / float(total_patches_seen+1)
        noisy_mean = noisy_patch.copy() if noisy_mean is None else (noisy_mean * total_patches_seen + noisy_patch) / float(total_patches_seen+1)

        # concatenate the patches to buffer the write
        noisy = noisy_patch if noisy is None else np.concatenate((noisy, noisy_patch), axis=0)
        clean = clean_patch if clean is None else np.concatenate((clean, clean_patch), axis=0)

        if patches_sampled == max_examples_per_file:
            print 'writing out files', filenum
            # write a new file
            write_out(noisy.astype('float32'), clean.astype('float32'), get_fname(filenum))
            filenum += 1
            # empty buffers
            data = None; label = None; patches_sampled = 0

    # write out book keeping files
    with open(os.path.join(out_dir, 'filelist.txt'), 'wb') as f:
        for i in xrange(filenum):
            f.write(get_fname(i) + '\n')

    # write out accumulated means
    with open(os.path.join(out_dir, 'means.pkl'), 'wb') as f:
        pkl.dump({'clean': clean_mean, 'noisy': noisy_mean}, f)
