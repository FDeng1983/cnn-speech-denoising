import sys
import argparse
import string

def main(argv):
   parser = argparse.ArgumentParser()
   parser.add_argument("replacements", nargs='+', help="replacements to make")
   args = parser.parse_args()

   pairs = [tuple(string.split(x,',',2)) for x in args.replacements]

   for line in sys.stdin:
      for x, y in pairs:
         line = line.replace(x,y)
      print line.rstrip("\n")


if __name__ == "__main__":
   main(sys.argv[1:])
