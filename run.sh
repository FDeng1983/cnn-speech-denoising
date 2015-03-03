#!/usr/bin/env bash

### Define your parameters here:

CAFFEDIR=~/caffe
DATASET=clean

LOGDIR=${CAFFEDIR}/project/cnn-speech-denoising/log

### Helper functions

NET=$DATASET

SPLITLOG=${LOGDIR}/${DATASET}.split.log
SAMPLELOG=${LOGDIR}/${DATASET}.sample.log
CAFFELOG=${LOGDIR}/${DATASET}.caffe.log

STARTDIR=$PWD

fail() {
  cd $STARTDIR
  exit 1
}

success() {
  cd $STARTDIR
  exit 0
}

cd_proj() {
    cd ${CAFFEDIR}/project/cnn-speech-denoising
}

cd_caffe() {
    cd ${CAFFEDIR}
}

split() {
    echo Splitting dataset to $SPLITLOG
    cd_proj

    # do a 70/30 split on the ${DATASET} dataset in to train and dev
    python split_dataset.py dataset/mfcc/${DATASET} > $SPLITLOG || fail
}

sample() {
    echo Sampling dataset to $SAMPLELOG
    cd_proj

    # sample the training data, normalize and dump the normalization params to disk
    python patch_sampler.py dataset/mfcc/${DATASET}/train --normalize_spec dataset/mfcc/${DATASET}/trained_normalization_params.pkl --scale_mfcc 1e-2 > $SAMPLELOG || fail

    # sample the dev data, normalize using the normalization params dumped during training
    python patch_sampler.py dataset/mfcc/${DATASET}/dev --normalize_spec dataset/mfcc/${DATASET}/trained_normalization_params.pkl --scale_mfcc 1e-2 --dev >> $SAMPLELOG || fail
}

train() {
    echo Training caffe to $CAFFELOG
    cd_caffe

    ./build/tools/caffe train \
        --solver=project/cnn-speech-denoising/models/model0/${NET}_solver.prototxt  > $CAFFELOG 2>&1 || fail
}



### Run what you want here:

mkdir -p $LOGDIR

# These two are destructive in that they are stochastic and will overwrite your splits and samples
# split
# sample

# This trains caffe
train

success
