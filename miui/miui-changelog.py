# -*- coding: utf-8 -*-  
import sys
import urllib2  
from sgmllib import SGMLParser
import re
import codecs

#thread-29693-1-20.html,  【2011年1月26日】MIUI第23周新年版发布说明- HD2模拟版发布

class URLLister(SGMLParser):
	is_a = ''
	names = []
	urls = []  
	def reset(self):   
		SGMLParser.reset(self)

	def start_a(self, attrs): 
		self.is_a = 1  
		href = [v for k, v in attrs if k=='href']   
		if href:  
			self.urls.extend(href)

	def end_a(self):
		self.is_a = ''

	def handle_data(self, text):
		if self.is_a:
			self.names.append(text)

def write_web_to_file(url, file_name):
	content = urllib2.urlopen(url)
	#if content.code == 200:
	#parser = URLLister()
	#parser.feed(content.read())
	output = open(file_name, 'w')
	output.write(content.read())
	output.close()
	content.close()

def get_changelog_thread(page_count):

	index_file = codecs.open("index.txt", 'w', 'utf-8')
	#index_file = open('index.txt', 'w')
	index_list = []
	for i in range(page_count): #22
		#m = re.match(r'.*l.*', ' hello world!')
		#print m
		#print .groups()
		post_list_file = open("page+%d.html" % (i+1), 'r')
		content = post_list_file.read()
		#rule =r".*<a href=\"(thread-\d*-1-\d*.html)\" style=\".*\">(.*第\d*周.*)</a>.*"
		#rule =r""".*<a href="(thread-\d*-1-\d*.html)" style=".*".*>(.*第\d*周.*)</a>.*"""
		#rule = re.compile(r".*(<a).*", re.S)
		rule = re.compile(r"""<a href="(thread-\d*-\d*-\d*.html)" style=".*?".*?>(.*?第\d*?周.*?)</a>""")
		results = rule.findall(content)

		#index_file.write("\r\n 第 %d 页:\r\n" % (i + 1))

		for j in range(len(results)):
			#index_file.write(codecs.BOM_UTF8.decode(str(results[j])))
			index_file.write(results[j][0])
			index_file.write(',  ')
			index_file.write(results[j][1])
			index_file.write('\r\n')
		#print rule.findall(content)[0]
		#pattern = re.compile(rule)
		#match = pattern.match(content)
		#match = re.match(r".*<a.*", 'aaa<a href></a>')
		#print match.groups
		post_list_file.close()

	index_file.close()

def get_changelogs():
	index_file = open("thread_index.txt")
	rule = re.compile(r"(thread-\d*-\d*-\d*.html), .*?第(\d*)周.*?")
	#rule = re.compile(r"(thread-\d*-\d*-\d*.html)")
	threads = rule.findall(index_file.read())
	
	for i in range(len(threads)):
		url = 'http://www.miui.com/' + threads[i][0]
		file_name = 'changelogs_raw/week' + threads[i][1] + '.htm'
		print 'write:' + file_name
		write_web_to_file(url, file_name)
	index_file.close()

def changelog_raw_to_txt():
	for i in range(153, 12, -1):
		

reload(sys) 
sys.setdefaultencoding( "utf-8" ) 
changelog_raw_to_txt()
