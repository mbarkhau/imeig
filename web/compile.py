#!/usr/bin/env python

import os

#find markbook
markbook_paths = (
    '/home/server/markbook/markbook.py',
    '/home/koloss/Dropbox/projects/markbook/markbook.py',
    '/home/mbarkhau/Ubuntu One/software_projects/markbook/markbook.py',
    '~/markbook/markbook.py',
    '~/bin/markbook.py',
)

markbook_cmd = ""
for p in markbook_paths:
    p = os.path.abspath(p)
    if os.path.exists(p):
        markbook_cmd = p
        break


base_dir = os.path.abspath(".")
#filter down dirs until only lang dirs are left

def is_lang_dir(d):
    return (os.path.isdir(d) and 
            os.path.exists(os.path.join(d, "metadata")))

lang_dirs = filter(is_lang_dir, os.listdir(base_dir))

for d in lang_dirs:
    print d

print os.system(markbook_cmd)
#/home/server/markbook/markbook.py

#cd /home/server/ie/web/de
#mv out.pdf IE.pdf
#zip ie_quellen.zip *.mkd metadata part1/* part2/*
