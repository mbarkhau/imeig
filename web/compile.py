#!/usr/bin/env python

import os

#find markbook
markbook_paths = (
    '/home/koloss/Dropbox/projects/markbook/markbook.py',
    '/home/server/markbook/markbook.py',
    '~/markbook/markbook.py',
    '~/bin/markbook.py',
)

markbook_cmd = ""
for p in markbook_paths:
    print p
    if os.path.exists(p):
        markbook_cmd = os.path.abspath(p)
        break


base_dir = os.path.abspath(".")
#filter down dirs until only lang dirs are left

def is_lang_dir(d):
    return (os.path.isdir(d) and 
            os.path.exists(os.path.join(d, "metadata")))

lang_dirs = filter(is_lang_dir, os.listdir(base_dir))

_ = os.system
_(markbook_cmd + " ".join(lang_dirs))
_("cd /home/server/ie/web/de")
_("mv out.pdf IE.pdf")
_("zip ie_quellen.zip *.mkd metadata part1/* part2/*")

