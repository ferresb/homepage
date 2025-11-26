#! /usr/bin/python
import argparse
import re
import json

from datetime import date

flag        = "data-translate"
TPE         = {"span", "link", "item", "pin", "domain", "me", "today", "navItem", "translate", "json"}
pattern     = re.compile('{{[^}]*}}')
langPH      = "__LANGUAGE__"
LINK_OUT    = "target=\"_blank\" rel=\"noopener noreferrer\""

MONTHS = { 1: {"english": "January", "french": "Janvier"},
           2: {"english": "February", "french": "Février"},
           3: {"english": "March", "french": "Mars"},
           4: {"english": "April", "french": "Avril"},
           5: {"english": "May", "french": "Mai"},
           6: {"english": "June", "french": "Juin"},
           7: {"english": "July", "french": "Juillet"},
           8: {"english": "August", "french": "Août"},
           9: {"english": "September", "french": "Septembre"},
          10: {"english": "October", "french": "Octobre"},
          11: {"english": "November", "french": "Novembre"},
          12: {"english": "December", "french": "Decembre"}}

DOMAINS = {
    "FPGA": "green",
    "DSE": "blue",
    "ERC": "red",
    "FM": "purple",
    "RTS": "gray",
    "Secu": "cyan",
    "Comp": "pink",
    "UArch": "black"
}

GOOGLE_SCHOLAR="https://scholar.google.fr/citations?user=x7_S3xAAAAAJ&hl=fr"

def switchLang(lang):
    return "french" if lang == "english" else "english"

class PlaceHolder:
    def __init__(self, args, config, string):
        url = args.src
        def findValue(key, default = None, error = False):
                def findall(key):
                    return re.compile('{}="[^"\r\n]+"'.format(key)).findall(string)
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
        self.color  = findValue("color", "blue")
        self.url    = url.split("/")[-1]
        self.out    = True if findValue("out") != None else False
        self.lang   = args.lang
        self.content = args.content
        try:
            self.text   = config[self.id].encode('utf-8')
        except:
            self.text   = None


    def toString(self):
        return "tpe: {}, id: {}, link: {}, class: {}".format(self.tpe, self.id, self.link, self.cls)

    def buildEntry(self):
        if self.tpe == "json":
            content = loadJson("{}/{}.json".format(self.content, self.id))
            columns = content['layout']['columns']
            entries = content['entries']
            html = ""
            for e in entries:
                row = "<div class=\"row\">\n"
                for c in columns:
                    if c['align'] == 'center':
                        entry = "<div class=\"col s{} center\">\n".format(c['size'])
                    else:
                        entry = "<div class=\"col s{}\">\n".format(c['size'])
                    match c['style']:
                        case 'normal':
                            pass
                        case 'bold':
                            entry += "<b>"
                        case _:
                            raise "Unknown style {}".format(c['style'])
                    for key in c['content']:
                        key = self.lang if key == 'CONTENT' else key
                        value = MONTHS[int(e[key])][self.lang] if (key == 'month') else e[key]
                        entry += "{} ".format(value)
                    row += "{}".format(entry)
                    match c['style']:
                        case 'normal':
                            pass
                        case 'bold':
                            row += "</b>"
                        case _:
                            raise "Unknown style {}".format(c['style'])
                    row += "\n</div>\n"
                html += row
                html += "</div>\n"
            return html
        if self.tpe == "navItem":
            self.link = ("{}_fr.html".format(self.link)) if self.lang == 'french' else ("{}_en.html".format(self.link))
        if self.tpe == "translate":
            if self.lang == "english":
                translateLink = self.url.replace("_en.html", "_fr.html")
            else:
                translateLink = self.url.replace("_fr.html", "_en.html")
        tmpId       = " id=\"" + self.id + "\"" if self.id else ""
        tmpClass    = " class=\"" + self.cls + "\"" if self.cls else ""
        tmpLink     = " href=\"" + self.link + "\"" if self.link else ""
        tmpText     = self.text.decode('utf8').replace("\n", "<br/>") if self.text else ""
        baseEntry   = "<span {}{}{}>{}</span>".format(flag, tmpId, tmpClass, tmpText)
        linkOut     = LINK_OUT if self.out else ""
        if self.tpe == "today":
            return "{}".format(date.today().strftime("%d/%m/%Y"))
        if self.tpe == "pin":
            return "<i class=\"material-icons {}-text\">blur_circular</i>".format(self.color)
        if self.tpe == "span":
            return baseEntry
        if self.tpe == "me":
            return "<a target=\"_blank\" rel=\"noopener noreferer\" href={} style=\"color: black\"><u>Bruno Ferres</u></a>".format(GOOGLE_SCHOLAR)
        if self.tpe == "domain":
            return "<b style=\"color: {}\">{}</b>".format(DOMAINS[self.id], self.id)
        if self.link == self.url:
            linkEntry   = "<a {}{}{}{}>{}</a>".format(flag, tmpId, tmpClass, linkOut, tmpText)
        else:
            linkEntry   = "<a {}{}{}{}{}>{}</a>".format(flag, tmpId, tmpLink, tmpClass, linkOut, tmpText)
        if self.tpe == "link":
            if self.link == self.url:
                return linkEntry
            else:
                return linkEntry
        if self.tpe == "item":
            if self.link == self.url:
                return "<li class=\"active\">{}</li>".format(linkEntry)
            else:
                return "<li>{}</li>".format(linkEntry)
        if self.tpe == "navItem":
            if self.link == self.url:
                return "<li class=\"active\">{}</li>".format(linkEntry)
            else:
                return "<li>{}</li>".format(linkEntry)
        if self.tpe == "translate":
            return "<li><a href=\"{}\"><img img-translate width=\"30\" src=\"images/{}.jpg\"/></a></li>".format(translateLink, switchLang(self.lang))

def loadJson(filename):
    f = open(filename)
    data = json.load(f)
    f.close()
    return data

def replace(args):
    config = loadJson("{}/{}.json".format(args.local, args.lang))
    f = open(args.src, 'r')
    srcLines = f.readlines()
    f.close()
    for i in range(0, len(srcLines)):
        for p in pattern.finditer(srcLines[i]):
            ph = PlaceHolder(args, config, p.group().replace("{{", "").replace("}}", ""))
            srcLines[i] = srcLines[i].replace(p.group(), ph.buildEntry())
    f = open(args.dest, 'w')
    for line in srcLines:
        f.write(line.replace(langPH, switchLang(args.lang)))
    f.close()

parser = argparse.ArgumentParser(description='Generate a web page from the templating system.')
parser.add_argument('src', metavar='source', type=str, help='The source file to use.')
parser.add_argument('dest', metavar='destination', type=str, help='The destination file to generate.')
parser.add_argument('local', metavar='local', type=str, help='The configuration folder for the languages.')
parser.add_argument('content', metavar='content', type=str, help='The folder containing the content as JSON files.')
parser.add_argument('--language', dest='lang', type=str, default='french', help='The default language for display. Default to french.')
parser.add_argument('--color', dest='color', type=str, default='green', help='The base color to be used. Default to green.')

replace(parser.parse_args())
