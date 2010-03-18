#!/usr/bin/python2.5
import getopt, sys, os

from os import path
from ConfigParser import SafeConfigParser

METAFILE_DEFAULT = "metadata.defaults"
METAFILE = "metadata"


def get_project_metadata(proj_dir):
    meta = SafeConfigParser()
    meta.readfp(open(METAFILE_DEFAULT))
    meta.read(METAFILE)
    #TODO: override options with those given in command line
    return meta


def separate(mkd):
    pass

def usage():
    print "help"


def filelist(proj_dir):
    files = os.listdir(proj_dir)
    files = [f for f in files if f.endswith(".mkd")]
    files = [os.path.join(proj_dir, f) for f in files]
    files.sort()
    return files


def assert_valid_project(proj_dir=os.path.abspath(".")):
    """ Expect a metadata file and some markdown files.
    
        Exits and emits error msg if dir is not a project
    """
    if not os.path.isdir(proj_dir):
        print "Directory not found: %s" % proj_dir
        sys.exit(2)

    if METAFILE not in os.listdir(proj_dir):
        print """Project requires a "metadata" file"""
        #TODO: generate one?
        sys.exit(2)
    
    if len(filelist(proj_dir)) == 0:
        print "No .mkd files in %s" % proj_dir
        sys.exit(2)


def is_heading(line, prev_line):
    """ Returns level, heading, if it is a heading, otherwise False."""

    if line.startswith("#"):
        level = line.count("#")
        return level, line[level:].strip()
    
    l = line.strip()
    if len(l) > 0 and len(l) in (l.count("-"), l.count("=")):
        level = 1 if line.count("=") else 2
        return level, prev_line.strip()

    return False


def parse(mkd):
    """ Splits the markdown into tuples of headings and paragraphs. """

    prev_line = ""
    heading = ""
    lvl = 0
    text = []
    contents = [] # elems (lvl, heading, text)

    # find headings and associate them with following text
    for line in mkd.splitlines(True):
        h = is_heading(line, prev_line)
        if h:
            contents.append((lvl, heading, "".join(text)))
            text = []
            prev_line = ""
            lvl, heading = h
        else:
            text.append(prev_line)
            prev_line = line
    
    # parse and remove metadata
    wo_meta = []
    metadata = {}
    for line in contents[0][2].splitlines(True):
        if wo_meta or not line.startswith("%"):
            # append if we have already started the post-metadata block
            # or if the line starts with the metadate char
            wo_meta.append(line)
        else:
            key, _, val = line.replace("%","").partition(":")
            metadata[key.strip()] = val.strip()

    contents[0] = (contents[0][0], contents[0][1], "".join(wo_meta))
    return metadata, contents


def parsefiles(proj_meta, filenames):
    doc = {}
    for f in filenames:
        fp = open(f)
        mkd = fp.read()
        fp.close()
        parse(mkd)
    return doc


def main(argv):                         
    try:
        optkeys = ["help", "verbose", "output=", "project_dir="]
        opts, args = getopt.getopt(argv, "hop:v", optkeys)
    except getopt.GetoptError, err:
        print "Error: %s\n" % err
        usage()
        sys.exit(2)

    files = args
    output = None
    verbose = False
    proj_dir = "."

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-p", "--project_dir"):
            proj_dir = arg
        elif opt in ("-p", "--project_dir"):
            proj_dir = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ('-o', "--output"):
            output = arg
        else:
            assert False, "unhandled option type"
    
    proj_dir = os.path.abspath(proj_dir)

    assert_valid_project(proj_dir)
    meta = get_project_metadata(proj_dir)
    filenames = filelist(proj_dir)
    doc = parsefiles(meta, filenames)

if __name__ == "__main__":
    main(sys.argv[1:])


"""
files = " ".join(filelist())

refname     = config.get("info", "refname")

title       = config.get("info", "title")
subtitle    = config.get("info", "subtitle")
authors     = config.get("info", "authors").split(",")
contribs    = config.get("info", "contributors").split(",")

html_cmd = "pandoc --toc -o web/%s.html %s" % (refname, files)
os.system(html_cmd)

#pdf_cmd = "markdown2pdf --custom-header=header_%s.template --toc -o IE_%s.pdf %s" % (lang, lang, files)
#os.system(pdf_cmd)
"""
