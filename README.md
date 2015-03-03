# cnn-speech-denoising

## Installation:

```bash
pip install docopt numpy h5py
# you also need to install caffe to ~/caffe
```

```bash
cd ~/caffe # go to your caffe directory
mkdir project
cd project
git clone https://github.com/vzhong/cnn-speech-denoising.git
```

## Dataset

This will give you the raw dataset we used, as well as the train/dev splits and sample patches we feed into the convnet.
```bash
cd cnn-speech-denoising/dataset
scp -r USERNAME@corn.stanford.edu:/scr/vzhong/cnn-speech-denoising/dataset/mfcc .
```

## Training:

```bash
# edit run.sh to reflect your configuration
./run.sh
```
