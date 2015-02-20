import htkmfc
import numpy as np
import sys
import argparse
import fnmatch

def main(argv):
   parser = argparse.ArgumentParser()
   parser.add_argument("input", help="input wav file")
   parser.add_argument("output", help="output mfcc file")
   args = parser.parse_args()

   data = np.loadtxt(args.input)
   w = htkmfc.HTKFeat_write(filename=args.output, veclen=39, paramKind=2886)
   print vars(w)
   w.writeheader()
   w.writeall(data)


if __name__ == "__main__":
   main(sys.argv[1:])
