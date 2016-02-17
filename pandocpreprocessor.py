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
        exmatch = expat.search(self.text)
        examples = list()
        while exmatch:
            ex = Example()
            rest = self.text[exmatch.end()+1:].splitlines()
            length = 1
            extext = exmatch.group(2)
            exlabel = exmatch.group(1)
            for line in rest:
                endmark = expat.match(line)
                if endmark:
                    #If a new example within the same paragraph
                    ex.NewEx(exlabel,extext)
                    extext = endmark.group(2)
                    exlabel = endmark.group(1)
                    length += len(line)
                elif line:
                    length += len(line)
                    extext += " " + line

                if not line:
                    ex.NewEx(exlabel,extext)
                    ex.End()
                    self.text = self.text[:exmatch.start()] + ex.string + self.text[exmatch.end()+length+1:]
                    examples.append(ex)
                    break

            exmatch = expat.search(self.text)

        for example in examples:
            self.text = example.AddReferences(self.text)


    def Finalize(self):
        with open('output.md','w') as f:
            f.write(self.text)

class Example():

    def __init__(self):
        self.string = ""
        self.labels = list()

    def NewEx(self,label, text):
       self.string += "\n" + r"\ex.\label{" + label + "} " + text + "\n"
       self.labels.append(label)

    def End(self):
        self.string += "\n\n"

    def AddReferences(self,text):
        for label in self.labels:
            pat = re.compile("@" + label + r"\b")
            text = pat.sub(r"\\ref{" + label + "}",text)

        return text



doc = Document(sys.argv[1],"tex")
doc.ConvertExamples()
doc.Finalize()


#print(m)

#expat.sub('',istr)


