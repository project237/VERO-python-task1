import argparse
from distutils import util

FILENAME = "vehicles.csv"

def main():
    parser = argparse.ArgumentParser(description='Print keys with color flag')
    parser.add_argument('-k', '--keys', nargs='+', help='input keys')
    parser.add_argument('-c', '--colored', default=True, help='colored flag', type=lambda x: bool(util.strtobool(x)))
    parser.add_argument('-f', '--filename', default="vehicles.csv", help='filename for csv', type=str)

    args = parser.parse_args()

    keys(*args.keys)

    print()

    # Print colored flag
    colored(args.colored)

    FILENAME = args.filename or FILENAME  
    print(FILENAME)

def keys(*args):
    for e in args:
        print(f"KEY: {e}")

def colored(is_colored):
    if is_colored:
        print("COLORED ON")
    else:
        print("COLORED OFF")

if __name__ == "__main__":
    main()

