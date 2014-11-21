# -*- coding: utf-8 -*-

import sys, os, re, codecs
import xlrd, xlwt
from xml.sax.handler import ContentHandler
from xml.sax import parse, make_parser, SAXException
from xml.etree import ElementTree as ET

def walk(indir):
    for root, dirs, files in os.walk(indir):
        for name in files:
            pathname = os.path.splitext(os.path.join(root, name))
            if pathname[1] == '.xml':
                transfer(os.path.join(root, name))


def transfer(xmlfile):
    xlsfile = xmlfile
    xlsfile = xlsfile.replace('.xml', '.xls')
    rex_match(xmlfile, xlsfile)


def rex_match(xmlfile, xlsfile):

    excel = xlwt.Workbook()
    sheet = excel.add_sheet('strings')

    re_str = '<string name="(\w*)"(\s.*?)*?>\s*(.*)\s*</string>'
    results = re.findall(re_str, codecs.open(xmlfile, 'r', 'utf-8').read())

    count = 0

    for item in results:
        sheet.write(count, 0, item[0])
        sheet.write(count, 1, item[-1])
        count += 1

    excel.save(xlsfile)

reload(sys)
sys.setdefaultencoding( "utf-8" )
if len(sys.argv) == 2:
    transfer(sys.argv[1])
else:
    walk('.')
