#!/usr/bin/python2.5

import os 
from ConfigParser import SafeConfigParser

METAFILE_DEFAULT = "metadata.defaults"
METAFILE = "metadata"

config = SafeConfigParser()
config.readfp(open(METAFILE_DEFAULT))
config.read(METAFILE)

def filelist():
    files = os.listdir(".")
    files = filter(lambda f: f.endswith(".mkd"), files)
    files.sort()
    return files

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
