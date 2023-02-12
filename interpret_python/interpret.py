import getopt, sys

from int_libs import shared

def main():
    long_options=["help", "source=", "input="]
    short_options="h"
    opts, args = getopt.getopt(sys.argv[1:], short_options, long_options)
    print(opts)




if __name__ == "__main__":
    main()