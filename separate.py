#!/usr/bin/python2.5
import getopt, sys, os

from os import path

from django.template import Template, Context
from django.conf import settings

settings.configure(
    DEBUG = False,
    TEMPLATE_DEBUG = False,
    TEMPLATE_DIRS = []
)

META_KEYS = ("refname", 
             "title",
             "subtitle",
             "authors",
             "contributors",
             "year")

SECTION_TMPL = "section.html.tmpl"

def get_section_tmpl(proj_dir):
    custom_tmpl = os.path.join(proj_dir, SECTION_TMPL)
    if os.path.isfile(custom_tmpl):
        tmpl = open(custom_tmpl)
    else:
        tmpl = open(SECTION_TMPL)
    return Template(tmpl.read())


def usage():
    print "help"


def filelist(proj_dir):
    files = os.listdir(proj_dir)
    files = [f for f in files if f.endswith(".mkd")]
    files = [os.path.join(proj_dir, f) for f in files]
    files.sort()
    return files


def assert_valid_project(proj_dir=os.path.abspath(".")):
    if not os.path.isdir(proj_dir):
        print "Directory not found: %s" % proj_dir
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
    # parse and remove metadata
    chapter = {}
    new_mkd = []
    for line in mkd.splitlines(True):
        if not new_mkd and line.startswith("%"):
            key, _, val = line.replace("%","").partition(":")
            chapter[key.strip()] = val.strip()
        else:
            # append if we have already started the post-metadata block
            # or if the line starts with the metadate char
            new_mkd.append(line)
    
    mkd = "".join(new_mkd)

    # find headings and associate them with following text
    prev_line = ""
    heading = ""
    lvl = 0
    text = []
    contents = [] # elems (lvl, heading, text)

    for line in mkd.splitlines(True):
        h = is_heading(line, prev_line)
        if h:
            text = "".join(text).strip()
            if text or heading:
                contents.append((lvl, heading, text))
            text = []
            prev_line = ""
            lvl, heading = h
        else:
            text.append(prev_line)
            prev_line = line

    # add the final paragraph (usually triggered by following one, which
    # doesn't exist in this case)
    contents.append((lvl, heading, "".join(text)))

    chapter["contents"] = contents 
    return chapter


def parsefiles(filenames):
    parts = []
    for f in filenames:
        fp = open(f)
        mkd = fp.read()
        fp.close()
        parts.append(parse(mkd))

    return parts


def gen_titlepage(doc):
    pass

def gen_section(id, chapter, title, text):
    pass

def gen_mkd(text):
    return text


PROJ = "projectcode"
TITLE = "title"
SUBTITLE = "subtitle"
AUTHORS = "authors"
CONTRIBS = "contributors"
DATE = "date"

CHAPTER = "chapter"

SECT_ID = "section_id"
PREV = "prev_id"
NEXT = "next_id"
SECT_TITLE = "section_title"
TEXT = "text"

mk_id = lambda lvl: ".".join([str(l) for l in lvl])

def compile(parts):
    out = []    # { id, prev, next, part, chapter, title, text }
    lvl = [0]   # expands to e.g [1, 2] for chapter 1 section 2
    ctx = {}

    cur_depth = 0

    for part in parts:
        cur_text = []

        if part.has_key(TITLE):
            lvl = lvl[0:1]
            cur_depth = 0
            ctx[TITLE] = part[TITLE]

        for depth, heading, text in part["contents"]:
            depth -= 1
            if cur_depth < depth:
                cur_depth += 1
                lvl.append(1)
            elif cur_depth > depth:
                lvl = lvl[:-1]
                cur_depth -= 1
                lvl[cur_depth] += 1
            else:
                lvl[-1] += 1

            if depth < 2:
                ctx[SECT_ID] = mk_id(lvl)
            if depth == 0:
                ctx[CHAPTER] = heading

            if depth > 1 and ctx[TEXT]:
                ctx[TEXT] += text
            else:
                ctx[TEXT] = text

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
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ('-o', "--output"):
            output = arg
        else:
            assert False, "unhandled option type"
    
    proj_dir = os.path.abspath(proj_dir)

    assert_valid_project(proj_dir)
    filenames = filelist(proj_dir)
    parts = parsefiles(filenames)
    compile(parts)
    tmpl = get_section_tmpl(proj_dir)

if __name__ == "__main__":
    main(sys.argv[1:])


"""
html_cmd = "pandoc --toc -o web/%s.html %s" % (refname, files)
os.system(html_cmd)

#pdf_cmd = "markdown2pdf --custom-header=header_%s.template --toc -o IE_%s.pdf %s" % (lang, lang, files)
#os.system(pdf_cmd)
"""
