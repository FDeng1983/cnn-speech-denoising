import sys
import argparse

def main(argv):
   parser = argparse.ArgumentParser()
   parser.add_argument("string_to_find", help="string to find")
   parser.add_argument("replacement", help="replacement string")
   args = parser.parse_args()

   for line in sys.stdin:
       print line.replace(args.string_to_find, args.replacement).rstrip('\n')


if __name__ == "__main__":
   main(sys.argv[1:])
