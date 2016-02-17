#!/usr/bin/env python3

import sys
import re

class Document():
    """The text that is transformed"""

    def __init__(self,fname,doctype):
        """Read text data etc """
        with open(fname,'r') as f:
            self.text = f.read()
        self.doctype = doctype

    def ConvertExamples(self):
        expat = re.compile(r'^ ?\(@(ee_[^\)]+)\)(.*)',re.MULTILINE)
        endpat = re.compile(r'(^ ?\(@(ee_[^\)]+)\).*|^$)',re.MULTILINE)
        for exmatch in expat.finditer(self.text):
            rest = self.text[exmatch.end()+1:].splitlines()
            for line in rest:
                endmark = endpat.match(line)
                if endmark:
                    #Either the next example or an empty line
                    self.text = self.text[:exmatch.start()] + self.WrapExe(exmatch.group(2),exmatch.group(1)) + self.text[exmatch.end()+1+endmark.start():]
                    #self.text = "{left}{right}".format(left="1",right="2")
                    break


    def Finalize(self):
        with open('output.{}'.format(self.doctype),'w') as f:
            f.write(self.text)


    def WrapExe(self, text, label):
        if self.doctype == 'tex':
            exestring =  "\n{}\n{}\n{}\n".format(r"\begin{exe}", r"\ex\label{" + label +"}" + text,  r"\end{exe}")

        return exestring



doc = Document(sys.argv[1],"tex")
doc.ConvertExamples()
doc.Finalize()


#print(m)

#expat.sub('',istr)


