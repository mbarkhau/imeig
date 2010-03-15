#!/usr/bin/python2.6

import os 

def filelist():
    files = os.listdir(".")
    files = filter(lambda f: f.endswith(".mkd"), files)
    files.sort()
    return files

files = " ".join(filelist())

print pdf_cmd

html_cmd = "pandoc --toc -o IE%s.html %s" % (lang, files)
#os.system(html_cmd)

#pdf_cmd = "markdown2pdf --custom-header=header_%s.template --toc -o IE_%s.pdf %s" % (lang, lang, files)
#os.system(pdf_cmd)
