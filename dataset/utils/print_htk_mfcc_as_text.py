import htkmfc
import numpy as np
import sys
import argparse

def main(argv):
   parser = argparse.ArgumentParser()
   parser.add_argument("input", help="input wav file")
   parser.add_argument("output", help="output mfcc file")
   args = parser.parse_args()

   r = htkmfc.HTKFeat_read(args.input)
   #print "Sample Period: {}".format(r.sampPeriod)
   print vars(r)
   data = r.getall()
   np.savetxt(args.output, data, fmt='%6.2f')



if __name__ == "__main__":
   main(sys.argv[1:])
