#!/usr/bin/env bash

### Define your parameters here:

DEFAULT_CAFFE_ROOT=~/scr/conv/caffe 
if [ -z "${CAFFE_ROOT}" ]; then
    CAFFE_ROOT=${DEFAULT_CAFFE_ROOT}
fi

DATASET=noisy_to_clean

LOGDIR=${CAFFE_ROOT}/project/cnn-speech-denoising/log

echo "Caffe root set to ${CAFFE_ROOT}"

### Helper functions

NET=$DATASET
DATAROOT=dataset/mfcc/conditions
MAXFILES=200
TIMESLICE=10
SCALE_MFCC=1

EXPTNAME=${DATASET}.${MAXFILES}

TRAINDIR=project/cnn-speech-denoising/${DATAROOT}/${EXPTNAME}/train/sampled
TESTDIR=project/cnn-speech-denoising/${DATAROOT}/${EXPTNAME}/dev/sampled

SPLITLOG=${LOGDIR}/${EXPTNAME}.split.log
SAMPLELOG=${LOGDIR}/${EXPTNAME}.sample.log
CAFFELOG=${LOGDIR}/${EXPTNAME}.caffe.log

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
    cd ${CAFFE_ROOT}/project/cnn-speech-denoising
}

cd_caffe() {
    cd ${CAFFE_ROOT}
}

split() {
    echo Splitting dataset to $SPLITLOG
    cd_proj

    # do a 70/30 split on the ${DATASET} dataset in to train and dev
    python split_dataset.py $DATAROOT/${DATASET} $DATAROOT/$EXPTNAME --max_files_to_process $MAXFILES > $SPLITLOG || fail
}

sample() {
    echo Sampling dataset to $SAMPLELOG
    cd_proj

    # sample the training data, normalize and dump the normalization params to disk
    python patch_sampler.py $DATAROOT/${EXPTNAME}/train --x_len $TIMESLICE > $SAMPLELOG || fail

    # sample the dev data, normalize using the normalization params dumped during training
    python patch_sampler.py $DATAROOT/${EXPTNAME}/dev --x_len $TIMESLICE >> $SAMPLELOG || fail
}

train() {
    echo Training caffe to $CAFFELOG
    cd_caffe

    cat project/cnn-speech-denoising/models/model0/${NET}.prototxt.template | \
	python project/cnn-speech-denoising/replace.py "+TEST_DIR+",${TESTDIR} | \
	python project/cnn-speech-denoising/replace.py "+TRAIN_DIR+",${TRAINDIR} > project/cnn-speech-denoising/models/model0/${EXPTNAME}.prototxt

    cat project/cnn-speech-denoising/models/model0/${NET}_solver.prototxt.template | \
	python project/cnn-speech-denoising/replace.py "+EXPT_NAME+",${EXPTNAME} > project/cnn-speech-denoising/models/model0/${EXPTNAME}_solver.prototxt

    ./build/tools/caffe train \
        --solver=project/cnn-speech-denoising/models/model0/${EXPTNAME}_solver.prototxt  > $CAFFELOG 2>&1 || fail
}



### Run what you want here:

mkdir -p $LOGDIR

# These two are destructive in that they are stochastic and will overwrite your splits and samples
split
sample

# This trains caffe
train

success
