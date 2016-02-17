#!/usr/bin/env python3

import sys
import re

class Document():
    """The text that is transformed"""

    Document.Tex

    def __init__(self,fname,doctype):
        """Read text data etc """
        with open(fname,'r') as f:
            self.lines = f.read().splitlines()
        self.doctype = doctype

    def ConvertExamples(self):
        expat = re.compile(r'^\s?\(@(ee_[^\)]+)\)')
        exstart = None
        exbegun = False
        for idx, line in enumerate(self.lines):
            exline = expat.match(line)
            if exbegun and (exline or not line):

            elif exline:
                exlabel = exline.group(1)
                exstart = exline.start()
                exbegun=True

        #for exstart in expat.finditer(self.text):
        #    import ipdb; ipdb.set_trace()

doc = Document(sys.argv[1],"tex")
doc.ConvertExamples()

#print(m)

#expat.sub('',istr)


