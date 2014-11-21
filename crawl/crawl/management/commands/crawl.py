# -*- coding: utf-8 -*-
import re
import urllib
import json
from bs4 import BeautifulSoup
import os
import shutil
from django.core.management.base import BaseCommand,CommandError
from web.models import Link
import datetime
import thread

website = 'http://nullnull-img.me/'
local = '/Users/liujiong/dev/crawl/datas/'

class Command(BaseCommand):
    def handle(self, *args, **options):
        flag = 1
        link = get_link(website)
        while (flag == 1):
            try:
                flag = parse(link)
            except:
                print 'catch exception.'


def parse(link):

    dest_dir = link.href.replace(website, local)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    html_doc = urllib.urlopen(link.href).read()

    re_a = r'\s*<a href="(\S*)">(\S*)</a>\s*(\d*-\w*-\d* \d\d:\d\d)\s*(\S*)'
    results = re.findall(re_a, html_doc)

    total = len(results)

    for item in results:

        item_link = get_link(link.href + item[0])
        if item_link.timestamp == item[2]:
            continue
        else:

            item_link.timestamp = item[2]
            item_link.size = item[3]

            if item[3] == '-':
                print 'parse   ', item_link.href, '%d/%d' % (results.index(item), total)
                parse(item_link)
                #item_link.save()
            else:
                print 'download', item_link.href, item[3], datetime.datetime.now().strftime("%H%M%S"), '%d/%d' % (results.index(item), total)
                #thread.start_new_thread(download, (item_link,) )
                download(item_link)

            item_link.save()

    return 0


def get_link(url):
    try:
        link = Link.objects.get(href=url)
    except:
        link = Link(href=url, size='-',
            timestamp=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        link.save()
    return link


def download(link):
    dest_file = link.href.replace(website, local)

    if os.path.basename(dest_file) == 'zip.zip': return
    #if url.index('http://nullnull-img.me/site00/gif/small/') >= 0: return
    #if url.index('http://nullnull-img.me/site00/movie/') >= 0: return
    #if link.href.index('http://nullnull-img.me/site00/small/') >= 0: return


    if not os.path.exists(os.path.dirname(dest_file)):
        os.mkdir(os.path.dirname(dest_file))
    urllib.urlretrieve(link.href, dest_file)

    link.save()
