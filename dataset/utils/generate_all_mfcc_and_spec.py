from subprocess import call
import os

dirs = [
    '/home/mkayser/school/classes/2014_2015_win/cs231n/proj/chime13/data/aasp-chime-grid/train/clean',
    '/home/mkayser/school/classes/2014_2015_win/cs231n/proj/chime13/data/aasp-chime-grid/train/isolated',
    '/home/mkayser/school/classes/2014_2015_win/cs231n/proj/chime13/data/aasp-chime-grid/devel/isolated',
    '/home/mkayser/school/classes/2014_2015_win/cs231n/proj/chime13/data/aasp-chime-grid/test/isolated']
        
for mydir in dirs:
    for mysubdir in os.listdir(mydir):
        path = '{}/{}'.format(mydir,mysubdir)
        command = ['octave', '--eval', '"iter_calc_mfcc {}"'.format(path)]
        print " ".join(command)
