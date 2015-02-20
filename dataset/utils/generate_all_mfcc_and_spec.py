from subprocess import call
import os

dirs = [
    '../aasp-chime-grid/train/clean',
    '../aasp-chime-grid/train/isolated',
    '../aasp-chime-grid/devel/isolated',
    '../aasp-chime-grid/test/isolated']
        
for mydir in dirs:
    for mysubdir in os.listdir(mydir):
        path = '{}/{}'.format(mydir,mysubdir)
        command = ['octave', '--eval', '"iter_calc_mfcc {}"'.format(path)]
        print " ".join(command)
