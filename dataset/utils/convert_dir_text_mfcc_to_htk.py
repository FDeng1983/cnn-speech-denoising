import htkmfc
import numpy as np
import sys
import argparse
import fnmatch
import os

def main(argv):
   MFCC_TXT_SUFF = ".mfcc"
   MFCC_HTK_SUFF = ".mfcc.htk"

   parser = argparse.ArgumentParser()
   parser.add_argument("inputdir", help="input directory")
   args = parser.parse_args()

   for f in os.listdir(args.inputdir):
      if(f.endswith(MFCC_TXT_SUFF)):
         path = args.inputdir + "/" + f
         outpath = path[:-len(MFCC_TXT_SUFF)] + MFCC_HTK_SUFF
         print path,outpath
         data = np.loadtxt(path)
         data = data[:,2:]
         w = htkmfc.HTKFeat_write(filename=outpath, veclen=39, paramKind=2886)
         w.writeheader()
         w.writeall(data)


if __name__ == "__main__":
   main(sys.argv[1:])
