#! /usr/bin/python
import argparse
import re
import json

flag    = "data-translate"
TPE     = {"span", "link", "item"}
pattern = re.compile('{{.*}}')

class PlaceHolder:
    def __init__(self, url, config, string):
        def findValue(key, default = None, error = False):
                def findall(key):
                    return re.compile('{}="[^" \r\n]+"'.format(key)).findall(string)
                def getInner(l, key, default):
                    if len(l) == 0:
                        if error:
                            raise Exception("Parameter {} is mandatory, but was not found in {}".format(key, string))
                        else:
                            return default
                    else:
                        return l[0].replace("{}=\"".format(key), "").replace("\"", "")
                return getInner(findall(key), key, default)
        self.tpe    = findValue("tpe", "span")
        if not self.tpe in TPE:
            raise Exception("Type {} unknown for entry {}".format(self.tpe, string))
        self.id     = findValue("id")
        self.link   = findValue("href")
        self.cls    = findValue("class")
        self.url    = url.split("/")[-1]
        try:
            self.text   = config[self.id].encode('utf-8')
        except:
            self.text   = None
        

    def toString(self):
        return "tpe: {}, id: {}, link: {}, class: {}".format(self.tpe, self.id, self.link, self.cls)

    def buildEntry(self):
        tmpId       = " id=\"" + self.id + "\"" if self.id else ""
        tmpClass    = " class=\"" + self.cls + "\"" if self.cls else ""
        tmpLink     = " href=\"" + self.link + "\"" if self.link else ""
        tmpText     = self.text if self.text else ""
        baseEntry   = "<span {}{}{}>{}</span>".format(flag, tmpId, tmpClass, tmpText)
        if self.tpe == "span":
            return baseEntry
        if self.link == self.url:
            linkEntry   = "<a {}{}{}>{}</a>".format(flag, tmpId, tmpClass, tmpText)
        else: 
            linkEntry   = "<a {}{}{}{}>{}</a>".format(flag, tmpId, tmpLink, tmpClass, tmpText)
        if self.tpe == "link":
            if self.link == self.url:
                return baseEntry
            else:
                return linkEntry
        if self.tpe == "item":
            if self.link == self.url:
                return "<li class=\"active\">{}</li>".format(linkEntry)
            else:
                return "<li>{}</li>".format(linkEntry)

def loadJson(args):
    f = open("{}/{}.json".format(args.local, args.lang))
    data = json.load(f)
    f.close()
    return data

def replace(args):
    config = loadJson(args)
    f = open(args.src, 'r')
    srcLines = f.readlines()
    f.close()
    for i in range(0, len(srcLines)):
        line = srcLines[i]
        for p in pattern.finditer(line):
            ph = PlaceHolder(args.src, config, p.group().replace("{{", "").replace("}}", "")) 
            srcLines[i] = line.replace(p.group(), ph.buildEntry())
    f = open(args.dest, 'w')
    for line in srcLines:
        f.write(line)
    f.close()     

parser = argparse.ArgumentParser(description='Generate a web page from the templating system.')
parser.add_argument('src', metavar='source', type=str, help='The source file to use.')
parser.add_argument('dest', metavar='destination', type=str, help='The destination file to generate.')
parser.add_argument('local', metavar='local', type=str, help='The configuration folder for the languages.')
parser.add_argument('--language', dest='lang', type=str, default='french', help='The default language for display. Default to french.')
parser.add_argument('--color', dest='color', type=str, default='green', help='The base color to be used. Default to green.')

replace(parser.parse_args())
