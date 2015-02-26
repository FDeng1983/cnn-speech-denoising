#!/usr/bin/env sh

if [ $# -eq 0 ]
then
	NET="auto_net"
else
	NET="$1"
fi


./build/tools/caffe train \
  --solver=project/cnn-speech-denoising/models/model0/${NET}_solver.prototxt
