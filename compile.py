#!/usr/bin/python2.5

import os 
from ConfigParser import SafeConfigParser

METAFILE_DEFAULT = "metadata.defaults"
METAFILE = "metadata"

config = SafeConfigParser()
config.readfp(open(METAFILE_DEFAULT))
config.read(METAFILE)

def filelist(lang):
    files = os.listdir("web/" + lang)
    files = filter(lambda f: f.endswith(".mkd"), files)
    files = [os.path.join("web", lang, f) for f in files]
    files.sort()
    return files

def compile(lang):
    files = " ".join(filelist(lang))

    db_cmd = "pandoc -s -S -w docbook -o web/%s/out.db %s" % (lang, files)
    html_cmd = "xmlto xhtml web/%s/out.db -o web/%s/html" % (lang, lang)

    tex_cmd = "pandoc --custom-header=web/%s/header.tex.tmpl -s -S --toc -o web/%s/%s.tex %s" % (lang, lang, lang, files)
    pdf_cmd = "pdflatex -output-directory web/%s web/%s/%s.tex" % (lang, lang, lang)

    #os.system(db_cmd)
    os.system(html_cmd)
    #os.system(tex_cmd)
    os.system(pdf_cmd)
    os.system(pdf_cmd) #2nd time for toc

#compile("de")
compile("en")
