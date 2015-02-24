#!/usr/bin/env sh

./build/tools/caffe train \
  --solver=project/cnn-speech-denoising/models/model0/auto_net_solver.prototxt
