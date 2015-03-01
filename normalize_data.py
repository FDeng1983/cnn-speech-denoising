#!/usr/bin/env python
""" normalize_data.py
Usage:
  normalize_data.py  <in_dir> <out_dir>
                    [--means=<means_pkl>]
                    [--log_transform]
                    [--verbose]
"""

import os
import numpy as np
import h5py
import cPickle as pkl

if __name__ == '__main__':
    from docopt import docopt
    args = docopt(__doc__)
    from pprint import pprint
    pprint(args)

    verbose = args['--verbose']

    if not os.path.isdir(args['<out_dir>']): os.makedirs(args['<out_dir>'])

    if args['--means']:
        print 'loading means'
        with open(args['--means']) as f:
            means = pkl.load(f)

        if args['--log_transform']:
            means['clean'] = np.log(means['clean'])
            means['noisy'] = np.log(means['noisy'])

    for fname in os.listdir(args['<in_dir>']):
        if fname.endswith('.h5'):
            in_fname = os.path.join(args['<in_dir>'], fname)
            out_fname = in_fname.replace(args['<in_dir>'].rstrip('/'), args['<out_dir>'].rstrip('/'))
            if verbose:
                print 'processing file', in_fname + '...',
            in_file = h5py.File(in_fname, 'r')

            noisy = in_file['data'].value
            clean = in_file['label'].value
            if args['--log_transform']:
                if verbose:
                    print 'log transform...',
                noisy = np.log(noisy)
                clean = np.log(clean)

            if args['--means']:
                if verbose:
                    print 'mean normalization...',
                noisy -= means['noisy']
                clean -= means['clean']

            if verbose:
                print
                print 'writing normalized file to', out_fname
            # HDF5 is pretty efficient, but can be further compressed.
            comp_kwargs = {'compression': 'gzip', 'compression_opts': 1}
            with h5py.File(out_fname, 'w') as f:
                f.create_dataset('data', data=noisy, **comp_kwargs)
                f.create_dataset('label', data=clean, **comp_kwargs)


