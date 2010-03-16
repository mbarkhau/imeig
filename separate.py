#!/usr/bin/python2.5
import getopt, sys

def usage():
    print "help"

def main(argv):                         
    try:
        opts = getopt.getopt(argv, "ho:v", ["help", "output="])
    except getopt.GetoptError, err:
        print "Error: %s\n" % err
        usage()
        sys.exit(2)

    output = None
    verbose = False
    print opts

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ('-o', "--output"):
            output = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
        else:
            assert False, "unhandled option type"

if __name__ == "__main__":
    main(sys.argv[1:])
