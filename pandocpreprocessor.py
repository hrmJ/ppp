#!/usr/bin/env python3
import sys
import re
from bs4 import BeautifulSoup

class Document():
    """The text that is transformed"""



    def __init__(self,fname,doctype):
        """Read text data etc """
        folder = '/home/juho/Dropbox/opetus/aspekti-ja-liikeverbiteoria/aihekokonaisuudet/'
        with open(folder + fname,'r') as f:
            self.text = f.read()
            lines = self.text.splitlines()

        ycount = 0
        self.yaml = ""

        for idx, line in enumerate(lines):
            self.yaml += line + "\n"
            if line[0:3] == '---':
                ycount += 1
            if ycount == 2:
                break

        self.text = "\n".join(lines[idx:])
        self.text = self.text[3:]

        self.doctype = doctype
        if doctype=="tex":
            self.text = self.text.replace("―","--")

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

    def HtmlCleaning(self):
        """Divs with clas definition"""
        soup = BeautifulSoup(self.text)
        #top bar
        bar = soup.find('article',{'id':'topbar'})
        if bar:
            bar.extract()
        #special headers
        bar = soup.find('p',{'class':'header'})
        if bar:
            bar.replaceWith("\chapter{" +  bar.text + "}\n")
        # css arrows
        arrows = soup.findAll('span',{'class':'right-arrow'})
        for arrow in arrows:
            arrow.replaceWith(arrow.text + r" \textrightarrow ")

        #colors

        #redcol = soup.findAll('span',{'class','r'})
        #for red in redcol:
        #    red.replaceWith(r'\color{red}' + red.text + r"}")

        self.text = str(soup)

        #html links:
        linkpat = re.compile(r'\([^\)]+\.html\#([^\)]+)\)')
        self.text = linkpat.sub(r'\1',self.text)



    def ConvertDefinitions(self):
        """Divs with clas definition"""
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

def ReplaceTagWithText(soup,tag,attrdict,replacement):
    arrows = soup.findAll(tag,attrdict)
    for arrow in arrows:
        arrow.replaceWith(arrow.text + r" \textrightarrow ")
    pass

def InsertDefinition(htext, dtext):
    """Insert a definition in tex"""
    beginning = r"\begin{maar}" + "\n"
    end = "\n" + r"\end{maar}"
    #return beginning + htext + ":" + r"\\" + dtext + end
    return beginning + dtext + end

docs = list()

for fname in sys.argv[1:]:
    doc = Document(fname,"tex")
    doc.HtmlCleaning()
    doc.ConvertExamples()
    doc.ConvertDefinitions()
    docs.append(doc)

#doc.Finalize()

fullstring = docs[0].yaml

for doc in docs:
    fullstring += "\n" + doc.text
 
with open('/home/juho/Dropbox/opetus/aspekti-ja-liikeverbiteoria/aihekokonaisuudet/aspektijaliikeverbiteoria.md','w') as f:
    f.write(fullstring)


