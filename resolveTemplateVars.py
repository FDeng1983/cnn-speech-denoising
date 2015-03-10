import re
import sys
import argparse
import string

CONV= """
layers {
  name: "+NAME+"
  type: CONVOLUTION
  bottom: "+BOTTOM+"
  top: "+TOP+"
  blobs_lr: 1
  blobs_lr: 2
  convolution_param {
    num_output: +D+
    kernel_h: +H+
    kernel_w: +W+
    stride: 1
    pad_h: +PH+
    pad_w: +PW+
    weight_filler {
      type: "xavier"
    }
    bias_filler {
      type: "constant"
    }
  }
}
"""

RELU= """
layers {
  name: "+NAME+"
  type: TANH
  bottom: "+BOTTOM+"
  top: "+TOP+"
}
"""

def makeNetString(spec):
   # example: c3x3_c5x5
   toks = string.split(spec,'_')
   
   layerStrings = []
   prevLayerOutput = "data"
   for i,t in enumerate(toks):
      isFinal = (i+1==len(toks))
      (prevLayerOutput, layerString) = makeLayerString(i,t,prevLayerOutput,isFinal)
      layerStrings.append(layerString)
   return string.join(layerStrings, "\n\n\n")
   
def makeLayerString(i, spec, prevOutput, isFinal):
   m = re.match(r'c(\d+)x(\d+)\.(\d+)(\.p(\d+)x(\d+))?$', spec)
   if m is not None:
      h = m.group(1)
      w = m.group(2)
      d = m.group(3)
      ph = m.group(5)
      pw = m.group(6)
      if ph is None: ph = str((int(h)-1)/2)
      if pw is None: pw = str((int(w)-1)/2)
      print "h,w,d,ph,pw = ", h, w, d, ph, pw
      name = "c{}".format(i)
      bottom = prevOutput
      top = "final_output" if isFinal else name

      layerString = (CONV.replace("+H+",h)
                         .replace("+W+",w)
                         .replace("+D+",d)
                         .replace("+PH+",ph)
                         .replace("+PW+",pw)
                         .replace("+NAME+",name)
                         .replace("+BOTTOM+",bottom)
                         .replace("+TOP+",top))

      return (name, layerString)


   m = re.match(r'r$', spec)
   if m is not None:
      name = "r{}".format(i)
      bottom = prevOutput
      top = "final_output" if isFinal else name

      layerString = (RELU.replace("+NAME+",name)
                         .replace("+BOTTOM+",bottom)
                         .replace("+TOP+",top))

      return (name, layerString)
   raise Exception("UnknownLayer")
      
def main(argv):
   parser = argparse.ArgumentParser()
   parser.add_argument("--net", help="neural net topology specifier string")
   parser.add_argument("infile", help="input file")
   parser.add_argument("outfile", help="output file")
   parser.add_argument("replacements", nargs='+', help="replacements to make")
   args = parser.parse_args()
   
   pairs = [tuple(string.split(x,',',2)) for x in args.replacements]
   
   if(args.net is not None):
      pairs.append(("+NET+", makeNetString(args.net)))

      
   with open(args.infile) as fin:
      with open(args.outfile, 'w') as fout:
         for line in fin:
            for x, y in pairs:
               line = line.replace(x,y)
            print >> fout, line.rstrip("\n")
                  
                  
if __name__ == "__main__":
   main(sys.argv[1:])

