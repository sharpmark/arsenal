from formatter import AbstractFormatter, NullWriter
from htmllib import HTMLParser
import codecs
import sys

#def _(str, in_encoder="utf-8", out_encoder="utf-8"):
#	return unicode(str, in_encoder).encode(out_encoder)

class myWriter(NullWriter):
	def __init__(self):
		NullWriter.__init__(self)
		self._bodyText = []

	def send_flowing_data(self, str):
		self._bodyText.append(str)

	def _get_bodyText(self):
		return '/n'.join(self._bodyText)
	
	bodyText = property(_get_bodyText, None, None, 'plain text from body')

class myHTMLParser(HTMLParser):
	def do_meta(self, attrs):
		self.metas = attrs

def convertFile(filename):
	mywriter = myWriter()
	absformatter = AbstractFormatter(mywriter)
	parser = myHTMLParser(absformatter)
	parser.feed(open(filename).read())
	return parser.formatter.writer.bodyText

import os
import os.path

reload(sys) 
sys.setdefaultencoding( "utf-8" ) 

OUTPUTDIR = "./changelogs_txt"
INPUTDIR = "./changelogs_raw"
if __name__ == "__main__":
	if not os.path.exists(OUTPUTDIR):
		os.mkdir(OUTPUTDIR)

	for filename in os.listdir(INPUTDIR):
		if filename[-4:] == '.htm':
			print "Coverting", filename,
			text = convertFile(os.path.join(INPUTDIR, filename))
			outfilename = filename + '.txt'
			outfullname = os.path.join(OUTPUTDIR, outfilename)
			out = codecs.open(outfullname, 'wt', 'utf-8')
			out.write(text)
			out.close()
			print "Done!"