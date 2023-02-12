import getopt, sys

from int_libs import scanner

def main():
    source_file = sys.stdin
    input_file = sys.stdin
    
    long_options=["help", "source=", "input="]
    short_options="h"
    opts, args = getopt.getopt(sys.argv[1:], short_options, long_options)
    for opt in opts:
        if opt[0] == "--help" or opt[0] == "-h":
            print("Zprava")
            exit(0)
        if opt[0] == "--input":
            source_file = opt[1]
        if opt[0] == "--source":
            input_file = opt[1]

    print("Source: ", source_file)
    print("Input: ", input_file)
    
    scanner.get_tokens(source_file)
    



if __name__ == "__main__":
    main()