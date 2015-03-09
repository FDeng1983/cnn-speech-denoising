#!/usr/bin/env bash

### Define your parameters here:
DEFAULT_CAFFE_ROOT=~/scr/conv/caffe 
if [ -z "${CAFFE_ROOT}" ]; then
    CAFFE_ROOT=${DEFAULT_CAFFE_ROOT}
fi

DATAROOT=dataset/autoencoder/conditions

DATASET=noisy_to_clean
NET=ae

### Helper functions

MAXFILES=$1
SAMPLES=$2
TIMESLICE=$3
LR=$4
GAMMA=$5
REG=$6
MAXITER=$7
NNARCH=$8

TESTSETSIZE=`python -c "print int($MAXFILES * $SAMPLES * .7)"`
LOSSWEIGHT=`python -c "print 1./($TIMESLICE*257)"`

echo "TEST SET SIZE: $TESTSETSIZE"
echo "LOSS WEIGHT: $LOSSWEIGHT"

DATACOND=ae_${DATASET}.f${MAXFILES}.s${SAMPLES}.t${TIMESLICE}
EXPTNAME=${DATACOND}.lr${LR}.g${GAMMA}.reg${REG}.iter${MAXITER}.nn_${NNARCH}

TRAINDIR=project/cnn-speech-denoising/${DATAROOT}/${DATACOND}/train/sampled
TESTDIR=project/cnn-speech-denoising/${DATAROOT}/${DATACOND}/dev/sampled

LOGDIR=${CAFFE_ROOT}/project/cnn-speech-denoising/log
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

    if [ ! -d $DATAROOT/$DATACOND ]; then
	# do a 70/30 split on the ${DATASET} dataset in to train and dev
	python autoenc_split_dataset.py $DATAROOT/${DATASET} $DATAROOT/$DATACOND --max_files_to_process $MAXFILES > $SPLITLOG || fail
    else
	echo "Reusing previous split()..."
    fi
}

sample() {
    echo Sampling dataset to $SAMPLELOG
    cd_proj

    if [ ! -d $DATAROOT/$DATACOND/train/sampled ]; then
	# sample the training data, normalize and dump the normalization params to disk
	python autoenc_patch_sampler.py $DATAROOT/${DATACOND}/train --augment_input --samples_per_file $SAMPLES --normalize_spec $DATAROOT/${DATACOND}/trained_normalization_params.pkl --x_len $TIMESLICE > $SAMPLELOG || fail

	# sample the dev data, normalize using the normalization params dumped during training
	python autoenc_patch_sampler.py $DATAROOT/${DATACOND}/dev --augment_input --samples_per_file $SAMPLES --normalize_spec $DATAROOT/${DATACOND}/trained_normalization_params.pkl --x_len $TIMESLICE --dev >> $SAMPLELOG || fail
    else
	echo "Reusing previous sample()..."
    fi
}

train() {
    echo Training caffe to $CAFFELOG
    cd_caffe

    in_net=project/cnn-speech-denoising/models/model0/${NET}.prototxt.template
    out_net=project/cnn-speech-denoising/models/model0/${EXPTNAME}.prototxt

    python project/cnn-speech-denoising/resolveTemplateVars.py --net $NNARCH $in_net $out_net \
	"+TEST_DIR+,${TESTDIR}" \
	"+TRAIN_DIR+,${TRAINDIR}" \
	"+LOSS_WEIGHT+,${LOSSWEIGHT}" 
	
    in_solver=project/cnn-speech-denoising/models/model0/${NET}_solver.prototxt.template
    out_solver=project/cnn-speech-denoising/models/model0/${EXPTNAME}_solver.prototxt

    python project/cnn-speech-denoising/resolveTemplateVars.py $in_solver $out_solver \
	"+EXPT_NAME+,${EXPTNAME}" \
	"+LEARNING_RATE+,${LR}" \
	"+GAMMA+,${GAMMA}" \
	"+MAX_ITER+,${MAXITER}" \
	"+REG+,${REG}" \
	"+TEST_SET_SIZE+,${TESTSETSIZE}" 
	
	

    ./build/tools/caffe train \
        --solver=project/cnn-speech-denoising/models/model0/${EXPTNAME}_solver.prototxt  > $CAFFELOG 2>&1 || fail
}



### Run what you want here:

mkdir -p $LOGDIR

# If the directory $DATAROOT/$DATACOND already exists, these will be no-ops and will reuse existing data
split
sample

# This trains caffe
train

success
