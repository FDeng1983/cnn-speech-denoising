#!/usr/bin/env python
""" patch_sampler.py
Usage:
  patch_sampler.py  <root_dir>
                    [--samples_per_file=5]
                    [--verbose]
                    [--augment_input]
                    [--x_len=20]
                    [--scale_mfcc=1]
                    [--random_seed=1003]
                    [--normalize_spec=<mean_std_dump_file>]
                    [--dev]

Options:

  --x_len=20                                how much in the time window do you want per patch [default: 20]

  --scale_mfcc=1                            what do you want to scale the input_spec labels by [default: 1]

  --samples_per_file=5                      how many samples you want to draw from each spectrogram input_spec pair [default: 5]

  --random_seed=1003                        seed for random number generator [default: 1003]

  --verbose                                 print logging information

  --augment_input                           append secondary information representing frequency to the input patch

  --normalize_spec=<mean_std_dump_file>     perform zero-mean, unit-variance normalization on the spectrograms. The mean and std
                                            will be calculated from the data and the result saved to <mean_std_dump_file>.

  --dev                                     if this is specified, then the mean and std will always be loaded from <mean_std_dump_file>
"""

import os
import numpy as np
import h5py
import cPickle as pkl


class SpectrogramPair(object):

    def __init__(self, input_spec_mat, output_spec_mat, num_samples, augment_input=False):
        try:
            with h5py.File(input_spec_mat, 'r') as f:
                self.input_spec_mat = f['ps/value'].value
                if augment_input:
                    orig = self.input_spec_mat
                    tempmatrix = np.tile(np.arange(float(orig.shape[1])),(orig.shape[0],1)) / float(orig.shape[1])
                    self.input_spec_mat = np.vstack((orig[None,...], tempmatrix[None,...]))
                else:
                    self.input_spec_mat = self.input_spec_mat.reshape((1,)+self.input_spec_mat.shape)

        except Exception as e:
            print 'Error in file', input_spec_mat
            raise e
        try:
            with h5py.File(output_spec_mat, 'r') as f:
                self.output_spec_mat = f['ps/value'].value
        except Exception as e:
            print 'Error in file', output_spec_mat
            raise e
        self.num_samples = num_samples

    def sample_patch(self, x_len):

        c_max, x_max, y_max = self.input_spec_mat.shape

        for i in xrange(self.num_samples):
            x_start = np.random.randint(low=0, high=x_max-x_len)

            input_spec_patch = self.input_spec_mat[:, x_start:x_start+x_len, :]
            output_spec_patch = self.output_spec_mat[x_start:x_start+x_len, :]

            assert output_spec_patch.shape == input_spec_patch.shape[1:]

            input_spec_patch = input_spec_patch[None,...]
            output_spec_patch = output_spec_patch[None,None,...]
            yield input_spec_patch, output_spec_patch


class PatchSampler(object):

    def __init__(self, input_spec_dir, output_spec_dir, samples_per_spectrogram=10, x_len=100, augment_input=False, verbose=False):
        self.input_spec_dir = input_spec_dir
        self.output_spec_dir = output_spec_dir
        self.n = samples_per_spectrogram
        self.x_len = x_len
        self.verbose = verbose
        self.augment_input = augment_input

    def __iter__(self):
        for root, dirs, files in os.walk(self.input_spec_dir, topdown=False):
            if self.verbose:
                print 'sampling from folder', root

            for name in files:
                if not name.endswith('.spec.hdf5'): continue

                input_spec = os.path.join(root, name)
                output_spec = input_spec.replace(self.input_spec_dir, self.output_spec_dir)
                assert os.path.isfile(input_spec),  "input spec file %s does not exist" % input_spec
                assert os.path.isfile(output_spec), "output spec file %s does not exist" % output_spec

                pair = SpectrogramPair(input_spec, output_spec, self.n, self.augment_input)
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

    x_len = int(args['--x_len'])
    samples_per_file = int(args['--samples_per_file'])
    seed = int(args['--random_seed'])

    np.random.seed(seed=seed)

    # where are the spectrograms
    root = args['<root_dir>']
    input_spec_dir = os.path.join(root, 'input_spec')
    output_spec_dir = os.path.join(root,  'output_spec')
    out_dir = os.path.join(root, 'sampled')
    if not os.path.isdir(out_dir): os.makedirs(out_dir)

    def get_fname(filenum):
        return os.path.join(out_dir, 'file.' + str(filenum) + '.h5')

    sampler = PatchSampler(input_spec_dir, output_spec_dir, samples_per_file, 
        verbose=args['--verbose'], x_len=x_len, augment_input=args['--augment_input'])

    input_spec = []; output_spec = []
    for input_spec_patch, output_spec_patch in sampler:

        # concatenate the patches to buffer the write
        input_spec  += [input_spec_patch]
        output_spec += [output_spec_patch]

    # Concatenate
    input_spec  = np.concatenate(input_spec, axis=0)
    output_spec = np.concatenate(output_spec, axis=0)

    print "input_spec shape: ", input_spec.shape
    print "output_spec shape: ", output_spec.shape

    if args['--dev']:
        assert args['--normalize_spec'], '--dev can only be used with --normalize_spec'
        with open(args['--normalize_spec'], 'rb') as f:
            print 'loading PREXISTING mean and std from', args['--normalize_spec']
            mean, std = pkl.load(f)


    input_spec_slice = input_spec[:,0,:,:]

    print "input_spec_slice shape: ", input_spec_slice.shape

    if args['--normalize_spec']:

        input_spec_slice = np.log(input_spec_slice)
        output_spec = np.log(output_spec)

        if not args['--dev']:
            print 'calculating mean and std from data'
            mean = input_spec_slice.mean(axis=0)
            std  = input_spec_slice.std(axis=0)

            print "mean shape: ", mean.shape
            print "std shape: ", std.shape
            print 'saving normalization paramters to', args['--normalize_spec']
            with open(args['--normalize_spec'], 'wb') as f:
                pkl.dump((mean, std), f)

        print 'normalizing input spectrograms'
        input_spec[:,0,:,:] = (input_spec_slice - mean) / std
        print 'normalizing output spectrograms'
        output_spec = (output_spec - mean) / std

    print 'observed input_spec maximum', input_spec[:,0,:,:].max(), 'minimum', input_spec[:,0,:,:].min()
    print 'observed output_spec maximum', output_spec.max(), 'minimum', output_spec.min()


    print 'writing out files'
    # write a new file
    write_out(input_spec.astype('float32'), output_spec.astype('float32'), get_fname(0))

    # write out book keeping files
    with open(os.path.join(out_dir, 'filelist.txt'), 'wb') as f:
        f.write('project/cnn-speech-denoising/' + get_fname(0) + '\n')

