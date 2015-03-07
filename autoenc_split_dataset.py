#!/usr/bin/env python
""" split_dataset.py

Splits dataset into train and dev sets

Usage:
    split_dataset.py  <root_dir> <output_dir>
                    [--train_portion=0.7]
                    [--max_files_to_process=0]

Options:
    --train_portion=0.7     how much of the data you want to use for training [default: 0.7]
    --max_files_to_process=0     how many input files to process [default: 0 => all files]
"""

import random
import shutil

class DatasetSplitter(object):

    def __init__(self, dirs):
        self.dirs = dirs
        

    def split_data(self, train_portion, max_files_to_process=0):
        all_files = []
        
        for root, dirs, files in os.walk(self.dirs['output_spec'], topdown=False):
            for name in files:
                if not name.endswith('.spec.hdf5'): continue

                output_spec = os.path.join(root, name)
                input_spec = output_spec.replace(self.dirs['output_spec'], self.dirs['input_spec'])

                assert os.path.isfile(output_spec)
                assert os.path.isfile(input_spec)

                all_files += [(input_spec, output_spec)]

        random.shuffle(all_files)
        if max_files_to_process != 0 and len(all_files)>max_files_to_process:
            all_files = all_files[:max_files_to_process]
        num_train = int(len(all_files) * train_portion)

        print num_train, 'out of', len(all_files), 'files will be used for training'

        for input_spec, output_spec in all_files[:num_train]:
            dest_spec = input_spec.replace(self.dirs['input_spec'], self.dirs['train/input_spec'])
            dest_output_spec = output_spec.replace(self.dirs['output_spec'], self.dirs['train/output_spec'])
            if not os.path.isdir(os.path.dirname(dest_spec)): os.makedirs(os.path.dirname(dest_spec))
            if not os.path.isdir(os.path.dirname(dest_output_spec)): os.makedirs(os.path.dirname(dest_output_spec))
            os.symlink(input_spec, dest_spec)
            os.symlink(output_spec, dest_output_spec)
            #shutil.copy(input_spec, dest_spec)
            #shutil.copy(output_spec, dest_output_spec)

        for input_spec, output_spec in all_files[num_train:]:
            dest_spec = input_spec.replace(self.dirs['input_spec'], self.dirs['dev/input_spec'])
            dest_output_spec = output_spec.replace(self.dirs['output_spec'], self.dirs['dev/output_spec'])
            if not os.path.isdir(os.path.dirname(dest_spec)): os.makedirs(os.path.dirname(dest_spec))
            if not os.path.isdir(os.path.dirname(dest_output_spec)): os.makedirs(os.path.dirname(dest_output_spec))
            os.symlink(input_spec, dest_spec)
            os.symlink(output_spec, dest_output_spec)
            #shutil.copy(input_spec, dest_spec)
            #shutil.copy(output_spec, dest_output_spec)


if __name__ == '__main__':
    import os
    from docopt import docopt
    from pprint import pprint
    args = docopt(__doc__)

    print 'User arguments'
    pprint(args)

    train_portion = float(args['--train_portion'])
    max_files_to_process = int(args['--max_files_to_process'])

    root = args['<root_dir>']
    out_dir = args['<output_dir>']
    dirs = {}
    
    random.seed(1001)

    for d in ['input_spec', 'output_spec']:
        dirs[d] = os.path.abspath(os.path.join(root, d))

    for d in ['train', 'dev']:
        d = os.path.join(out_dir, d)
        if os.path.isdir(d):
            print 'removing directory', d, 'for resampling'
            shutil.rmtree(d)

    for d in ['train', 'dev', 'train/input_spec', 'train/output_spec', 'dev/input_spec', 'dev/output_spec']:
        dirs[d] = os.path.join(out_dir, d)
        if not os.path.isdir(dirs[d]):
            print 'making directory', dirs[d]
            os.makedirs(dirs[d])

    splitter = DatasetSplitter(dirs)
    splitter.split_data(train_portion, max_files_to_process)

