import h5py
import os
import numpy
import sys
import argparse
import fnmatch

def main(argv):
   parser = argparse.ArgumentParser()
   parser.add_argument("inputdir", help="input dir")
   args = parser.parse_args()

   for root, dirs, files in os.walk(args.inputdir):
      for name in files:
         if name.endswith('mfcc.hdf5'):
            loc = os.path.join(root,name)
            f = h5py.File(loc,'r')
            m = f['mfc/value']
            print numpy.min(m), numpy.max(m)
            f.close()


if __name__ == "__main__":
   main(sys.argv[1:])
