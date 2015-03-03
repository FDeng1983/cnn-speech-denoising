#!/usr/bin/env python
""" split_dataset.py

Splits dataset into train and dev sets

Usage:
    split_dataset.py  <root_dir>
                    [--train_portion=0.7]

Options:
    --train_portion=0.7     how much of the data you want to use for training [default: 0.7]
"""
import random
import shutil

class DatasetSplitter(object):

    def __init__(self, dirs):
        self.dirs = dirs

    def split_data(self, train_portion):
        all_files = []
        for root, dirs, files in os.walk(self.dirs['mfcc'], topdown=False):
            for name in files:
                if not name.endswith('.hdf5'): continue

                mfcc = os.path.join(root, name)
                spec = mfcc.replace(self.dirs['mfcc'], self.dirs['spec']).replace('wav.mfcc', 'wav.spec')

                assert os.path.isfile(mfcc)
                assert os.path.isfile(spec)

                all_files += [(spec, mfcc)]

        random.shuffle(all_files)
        num_train = int(len(all_files) * train_portion)

        print num_train, 'out of', len(all_files), 'files will be used for training'

        for spec, mfcc in all_files[:num_train]:
            shutil.copy(spec, spec.replace(self.dirs['spec'], self.dirs['train/spec']))
            shutil.copy(mfcc, mfcc.replace(self.dirs['mfcc'], self.dirs['train/mfcc']))

        for spec, mfcc in all_files[num_train:]:
            shutil.copy(spec, spec.replace(self.dirs['spec'], self.dirs['dev/spec']))
            shutil.copy(mfcc, mfcc.replace(self.dirs['mfcc'], self.dirs['dev/mfcc']))


if __name__ == '__main__':
    import os
    from docopt import docopt
    from pprint import pprint
    args = docopt(__doc__)

    print 'User arguments'
    pprint(args)

    train_portion = float(args['--train_portion'])

    root = args['<root_dir>']
    dirs = {}

    for d in ['spec', 'mfcc']:
        dirs[d] = os.path.join(root, d)

    for d in ['train', 'dev']:
        d = os.path.join(root, d)
        if os.path.isdir(d):
            print 'removing directory', d, 'for resampling'
            shutil.rmtree(d)

    for d in ['train', 'dev', 'train/spec', 'train/mfcc', 'dev/spec', 'dev/mfcc']:
        dirs[d] = os.path.join(root, d)
        if not os.path.isdir(dirs[d]):
            print 'making directory', dirs[d]
            os.makedirs(dirs[d])

    splitter = DatasetSplitter(dirs)
    splitter.split_data(train_portion)

