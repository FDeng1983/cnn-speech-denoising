#!/usr/bin/env bash

### Define your parameters here:

CAFFEDIR=~/caffe
DATASET=noisy

LOGDIR=~/caffe/log

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
    cd_proj

    # do a 70/30 split on the ${DATASET} dataset in to train and dev
    python split_dataset.py dataset/mfcc/${DATASET} > $SPLITLOG || fail
}

sample() {
    cd_proj

    # sample the training data, normalize and dump the normalization params to disk
    python patch_sampler.py dataset/mfcc/${DATASET}/train --normalize_spec dataset/mfcc/${DATASET}/trained_normalization_params.pkl --scale_mfcc 1e-2 > $SAMPLELOG || fail

    # sample the dev data, normalize using the normalization params dumped during training
    python patch_sampler.py dataset/mfcc/${DATASET}/dev --normalize_spec dataset/mfcc/${DATASET}/trained_normalization_params.pkl --scale_mfcc 1e-2 --dev >> $SAMPLELOG || fail
}

train() {
    cd_caffe

    ./build/tools/caffe train \
        --solver=project/cnn-speech-denoising/models/model0/${NET}_solver.prototxt  > $CAFFELOG 2>&1 || fail
}



### Run what you want here:

mkdir $LOGDIR

echo Splitting dataset to $SPLITLOG

split

echo Sampling dataset to $SAMPLELOG

sample

echo Training caffe to $CAFFELOG

train

success