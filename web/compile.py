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
    if os.path.exists(p):
    	print p
        markbook_cmd = os.path.abspath(p)
        break


base_dir = os.path.abspath(".")
#filter down dirs until only lang dirs are left

def is_lang_dir(d):
    return (os.path.isdir(d) and 
            os.path.exists(os.path.join(d, "metadata")))

lang_dirs = filter(is_lang_dir, os.listdir(base_dir))

_ = os.system

for l in lang_dirs:
    _(markbook_cmd + " " + l)
    _("mv out.pdf %s/IE.pdf" % l)
    _("rm %s/out.*" % l)
    _("rm out.*")
    _("zip %s/ie_quellen.zip %s/*.mkd %s/metadata %s/part1/* %s/part2/*" % (l,l,l,l,l))
