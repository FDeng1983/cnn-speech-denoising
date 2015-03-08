#!/usr/bin/env python
""" predict.py

Usage:
    predict.py <input_spec> <normalization_pkl> <output_hdf5> <prototxt> <caffemodel>
                [--cpu]
                [--mfcc=<mfcc_hdf5>]
"""

from docopt import docopt
from pprint import pprint
import os

# python predict.py dataset/mfcc/noisy/spec/bgbu4p.wav.spec.hdf5 dataset/mfcc/conditions/noisy_to_clean.200/trained_normalization_params.pkl pred.h5 models/model0/noisy_to_clean.200.prototxt models/model0/snapshots/noisy_to_clean.200_iter_200.caffemodel --mfcc dataset/mfcc/noisy/mfcc/bgbu4p.wav.mfcc.hdf5

if __name__ == '__main__':

    args = docopt(__doc__)

    normalization = os.path.abspath(args['<normalization_pkl>'])
    model_file = os.path.abspath(args['<prototxt>'])
    pretrained = os.path.abspath(args['<caffemodel>'])
    input_hdf5 = os.path.abspath(args['<input_spec>'])
    label_hdf5 = os.path.abspath(args['--mfcc']) if args['--mfcc'] else None
    output_hdf5 = os.path.abspath(args['<output_hdf5>'])

    import cPickle as pkl
    with open(normalization) as f:
        mean, std = pkl.load(f)

    if 'CAFFE_ROOT' in os.environ:
        caffe_root = os.environ['CAFFE_ROOT']
    else:
        caffe_root = os.path.abspath(os.path.join(os.getcwd(), '..', '..'))
        print '$CAFFE_ROOT is unspecified! Assuming $CAFFE_ROOT is', caffe_root

    assert os.path.isdir(caffe_root)
    orig_dir = os.getcwd()
    os.chdir(caffe_root)

    print 'user args:'
    pprint(args)

    import numpy as np
    import sys
    sys.path.insert(0, caffe_root + 'python')
    import caffe

    if args['--cpu']:
        caffe.set_mode_cpu()
    else:
        caffe.set_mode_gpu()

    print 'loading pretrained model in test mode'

    # train mode is 0, test is 1
    net = caffe.Net(model_file, pretrained, 1)

    print 'net has layers'
    pprint(net.blobs.keys())

    input_layer = net.blobs.keys()[0]
    output_layer = net.blobs.keys()[-2]

    print 'assuming input layer', "'" + input_layer + "'"
    print 'assuming output layer', "'" + output_layer + "'"

    print 'loading input data'

    import h5py
    with h5py.File(input_hdf5) as f:
        X = np.log(f['ps/value'].value)
    print 'input data has shape', X.shape

    batch_start = 0
    batch_shape = net.blobs[input_layer].data.shape

    print 'reshaping: batch_shape', batch_shape, 'data_shape', X.shape

    def split_patches(X, y_len, batch_size):
        pad_y = y_len - X.shape[0] % y_len
        X = np.concatenate([X, np.zeros((pad_y, X.shape[1]))], axis=0)
        patches = []

        y_start = 0
        while y_start < X.shape[0]:
            y_end = y_start + y_len
            patch = X[y_start:y_end, :]
            reshaped = patch.reshape((1, 1, y_len, X.shape[1]))
            patches += [reshaped]
            y_start = y_end

        patches = np.concatenate(patches, axis=0)
        pad_batches = batch_size - patches.shape[0] % batch_size

        pad_shape = list(patches.shape)
        pad_shape[0] = pad_batches

        patches = np.concatenate([patches, np.zeros(pad_shape)], axis=0)

        return patches, pad_y, pad_batches

    patches, pad_y, pad_batches = split_patches(X, batch_shape[2], batch_shape[0])
    print 'new data shape', patches.shape
    assert patches.shape[1:] == batch_shape[1:]

    def normalize(batch, mean, std):
        assert batch.shape[1:] == mean.shape[:], 'mean has shape ' + str(mean.shape) + ' but batch has shape ' + str(batch.shape)
        assert batch.shape[1:] == std.shape[:], 'std has shape ' + str(std.shape) + ' but batch has shape ' + str(batch.shape)
        for i in range(batch.shape[0]):
            batch[i] = (batch[i] - mean) / std
        return batch

    print 'predicting...'
    pred = None

    def save_temp(net):
        net.save('temp.caffemodel')

    def load_temp():
        return caffe.Net(model_file, 'temp.caffemodel', 1)

    while batch_start < patches.shape[0]:
        batch_end = batch_start + batch_shape[0]
        batch = patches[batch_start:batch_end]
        batch = normalize(batch, mean, std)
        net.blobs[input_layer].data[...] = (batch - mean) / std

        # super clunky
        # save_temp(net)
        # net = load_temp()

        net.forward()

        out = net.blobs[output_layer].data.copy()
        pred = out if pred is None else np.concatenate([pred, out], axis=0)
        batch_start += batch_shape[0]

    def stitch_patches(Y, y_len, pad_y, pad_batches):
        Y = Y.copy()
        # throw away pad batches
        Y = Y[:-pad_batches, :, 0, 0]
        pred = Y.reshape((Y.shape[0]*y_len, Y.shape[1]/y_len))

        # remove y padding
        pred = pred[:-pad_y, :]
        return pred

    # remove predictions for padding
    pred = stitch_patches(pred, batch_shape[2], pad_y, pad_batches)

    if label_hdf5:
        with h5py.File(label_hdf5) as f:
            labels = f['mfc/value'].value
        print pred
        print
        print
        print labels
        print 'MSE', np.sum((pred - labels)**2, axis=1).mean(axis=0)

    print 'writing out predictions', pred.shape
    comp_kwargs = {'compression': 'gzip', 'compression_opts': 1}
    with h5py.File(output_hdf5, 'w') as f:
        f.create_dataset('data', data=X, **comp_kwargs)
        f.create_dataset('label', data=pred, **comp_kwargs)
