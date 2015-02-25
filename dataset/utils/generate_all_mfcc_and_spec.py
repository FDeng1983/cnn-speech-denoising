from subprocess import call
import os

dirs = [
    '/juicer/scr81/scr/mkayser/conv/cnn-speech-denoising/dataset/aasp-chime-grid/train/clean',
    '/juicer/scr81/scr/mkayser/conv/cnn-speech-denoising/dataset/aasp-chime-grid/train/isolated',
    '/juicer/scr81/scr/mkayser/conv/cnn-speech-denoising/dataset/aasp-chime-grid/devel/isolated',
    '/juicer/scr81/scr/mkayser/conv/cnn-speech-denoising/dataset/aasp-chime-grid/test/isolated']
        
for mydir in dirs:
    for mysubdir in os.listdir(mydir):
        path = '{}/{}'.format(mydir,mysubdir)
        command = ['matlab', '-r', '"iter_calc_mfcc {}"'.format(path)]
        print " ".join(command)
