#!/usr/bin/env python3
import sys
import re
from bs4 import BeautifulSoup

class Document():
    """The text that is transformed"""



    def __init__(self,fname,doctype):
        """Read text data etc """
        if type(fname) == 'list':
        else:
            with open(fname,'r') as f:
                self.text = f.read()
                lines = self.text.splitlines()
        #ycount = 0
        #self.yaml = ""

        #for idx, line in enumerate(lines):
        #    self.yaml += line + "\n"
        #    if line[0:3] == '---':
        #        ycount += 1
        #    if ycount == 2:
        #        break

        #self.text = "\n".join(lines[idx:])
        #self.text = self.text[3:]
        #self.text = self.text[3:8]

        self.doctype = doctype
        if doctype=="tex":
            self.preamp = r"""\documentclass[a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[T2A]{fontenc}
\usepackage[finnish]{babel}
\usepackage{linguex} 
\usepackage{amsthm}
\newtheorem{maar}{Määritelmä}"""

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

    def ConvertDefinitions(self):
        """Divs with clas definition"""
        #divpat = re.compile(r'.*<div .*definition.*')
        #kkl
        soup = BeautifulSoup(self.text)
        defdivs = soup.findAll('div',{'class':'definition'})
        for div in defdivs:
            header = div.find('div',{'class','defheader'})
            headertext = header.text
            header.extract()
            div.replaceWith(InsertDefinition(headertext,div.text))
        self.text = str(soup)
        self.text = self.text.replace('<html><body><p>','')
        self.text = self.text.replace(r'</p></body></html>','')
        self.text = self.text.replace('<html><body>','')
        self.text = self.text.replace(r'</body></html>','')


    def Finalize(self):
        with open('output.md','w') as f:
            #f.write("{}\n\n{}\n\n{}\n{}\n{}".format(self.yaml, self.preamp, r"\begin{document}" + "\n",self.text,r"\end{document}"))
            f.write(self.text)


class Example():
    """Linguistic example replacing @ee_"""
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


def InsertDefinition(htext, dtext):
    """Insert a definition in tex"""
    beginning = r"\begin{maar}" + "\n"
    end = "\n" + r"\end{maar}"
    #return beginning + htext + ":" + r"\\" + dtext + end
    return beginning + dtext + end

doc = Document(sys.argv[1],"tex")
doc.ConvertExamples()
doc.ConvertDefinitions()
doc.Finalize()


#print(m)

#expat.sub('',istr)


