#!/usr/bin/python2.6

import os 

lang = "de"

def filelist(lang="de"):
    files = os.listdir(".")
    files = filter(lambda f: "_" + lang + "_" in f, files)
    files = filter(lambda f: f.endswith(".mkd"), files)
    files.sort()
    return files

files = " ".join(filelist(lang))

html_cmd = "pandoc --toc -o IE_%s.html %s" % (lang, files)
pdf_cmd = "markdown2pdf --custom-header=header_%s.template --toc -o IE_%s.pdf %s" % (lang, lang, files)

print pdf_cmd

os.system(html_cmd)
os.system(pdf_cmd)
