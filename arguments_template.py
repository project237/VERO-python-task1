# run ths file with:
#   python arguments_template.py -k key1 key2 key3 -c 0 

import argparse
from distutils import util
from pprint import pprint

INPUT_FILE = "vehicles.csv"
KEYS     = []
COLORED  = True

def main():
    parser = argparse.ArgumentParser(description='Print keys with color flag')
    parser.add_argument('-k', '--keys', nargs='+', help='input keys')
    parser.add_argument('-c', '--colored', default=True, help='colored flag', type=lambda x: bool(util.strtobool(x)))
    # parser.add_argument('-f', '--filename', default="vehicles.csv", help='filename for csv', type=str)
    # INPUT_FILE = args.filename or INPUT_FILE  
    # print(INPUT_FILE)

    args    = parser.parse_args()
    KEYS    = args.keys
    COLORED = args.colored

    pprint(args)
    print()
    pprint(KEYS)
    print()
    pprint(COLORED)

if __name__ == "__main__":
    main()

