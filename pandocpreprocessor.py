#!/usr/bin/env python3

import sys
import re

class Document():
    """The text that is transformed"""

    def __init__(self,fname,doctype):
        """Read text data etc """
        with open(fname,'r') as f:
            self.text = f.read().splitlines()
        self.doctype = doctype

    def ConvertExamples(self):
        expat = re.compile(r'^\s?\(@(ee_[^\)]+)\)',re.MULTILINE)

        #for exstart in expat.finditer(self.text):
        #    import ipdb; ipdb.set_trace()

doc = Document(sys.argv[1],"tex")
doc.ConvertExamples()

#print(m)

#expat.sub('',istr)


