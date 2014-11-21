# -*- coding: utf-8 -*-
import re
import urllib
import json
from bs4 import BeautifulSoup
from web.models import Link

def parse_url(url, root):

    #if Link.objects.filter(href=url).count() < 1: return

    html_doc = urllib.urlopen(url).read()
    soup = BeautifulSoup(html_doc)

    for a in soup.find_all('a'):
        link = a.get('href')

        if link[0] == '?': continue
        if a.string == 'Parent Directory': continue
        if link[-3:] in('jpg', 'png', 'gif', 'zip', 'tml'): download(link)
        parse_url(link)

def download(url):
    pass

parse_url('http://nullnull-img.me/')
