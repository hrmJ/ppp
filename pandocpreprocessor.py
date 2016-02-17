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
            self.text = f.read()
        self.doctype = doctype

    def ConvertExamples(self):
        expat = re.compile(r'^\s?\(@(ee_[^\)]+)\)',re.MULTILINE)
        exstart = None
        exbegun = False
        for exstart in expat.finditer(self.text):
            import ipdb; ipdb.set_trace()


doc = Document(sys.argv[1],"tex")
doc.ConvertExamples()

#print(m)

#expat.sub('',istr)


