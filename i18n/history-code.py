# -*- coding: utf-8 -*-  

import sys, xlrd, xlwt
from PIL import Image
from xml.sax.handler import ContentHandler
from xml.sax import parse
from xml.etree import ElementTree as ET

def handle_lockscreen_2():
    #print zangwen, zhongwen, excel
    excel = xlwt.Workbook()
    sheet = excel.add_sheet('strings')

    cn_xml = ET.parse('./timer/strings_cn.xml')
    cn_strings = cn_xml.findall('./string')

    en_xml = ET.parse('./timer/strings_en.xml')
    en_strings = en_xml.findall('./string')

    for i in range(len(cn_strings)):
        sheet.write(i, 0, cn_strings[i].text)
        sheet.write(i, 1, en_strings[i].text)

    excel.save('timer.xls')
def handle_lockscreen():
    #print zangwen, zhongwen, excel
    excel = xlwt.Workbook()
    sheet = excel.add_sheet('strings')

    cn_xml = ET.parse('./timer2/strings.xml')
    cn_strings = cn_xml.findall('./string')

    for i in range(len(cn_strings)):
        sheet.write(i, 0, cn_strings[i].attrib['name'])
        if list(cn_strings[i]) == []:
            sheet.write(i, 1, cn_strings[i].text)
        else:
            content = re.compile(r'^<string[^>]+>(?P<text>.+?)</string>.*')

            xmlstr = ET.tostring(cn_strings[i])
            sheet.write(i, 1, content.match(xmlstr).groups('text')[0].encode('utf8'))

    excel.save('timer2.xls')
def handle_zangwen(zangwen_file, zhongwen_file, excel_file):
	#print zangwen, zhongwen, excel
	try:
		if os.path.exists(zangwen_file) and os.path.exists(zhongwen_file):
			excel = xlwt.Workbook()
			sheet = excel.add_sheet('strings')

			zang_xml = ET.parse(zangwen_file)
			zang_strings = zang_xml.findall('./string')

			zhong_xml = ET.parse(zhongwen_file)
			zhong_strings = zhong_xml.findall('./string')

			for i in range(len(zhong_strings)):
				#print zhong_strings[i].text
				#print zhong_strings[i].value
				sheet.write(i, 0, zhong_strings[i].text)
				sheet.write(i, 1, zang_strings[i].text)

			excel.save(excel_file)
	except Exception, e:
		print zangwen_file, zhongwen_file, excel_file

	for d in dirs:

		if d <> '.DS_Store':

			for f in os.listdir(os.path.join('./gaka/rcn', d)):
				fn = os.path.splitext(f)[0]

				zangwen_file   = filename_format % {'lang':'rcn', 'dir':d, 'filename':fn, 'ext':'xml'}
				zhongwen_file  = filename_format % {'lang':'scn', 'dir':d, 'filename':fn, 'ext':'xml'}
				excel_file     = filename_format % {'lang':'output', 'dir':'.', 'filename':d + fn, 'ext':'xls'}
				#zhongwen_file = filename_format % {'lang':'scn', 'dir':d, 'filename':fn, 'ext':'xml'}
				#excel_file = filename_format % {'lang':'output', 'dir':'.', 'filename':fn, 'ext':'xls'}

				handle_zangwen(zangwen_file, zhongwen_file, excel_file)
def handle_go_2():
	langlist = ['de', 'fr',]
	filelist = [u'OTA', u'计算器', u'时钟', u'电话', u'便签', u'启动器', u'Framework', u'锁屏', u'设置', u'相机&相册', u'联系人', u'短信']

	for lang in langlist:
		print '====process language:' + lang

		# read excel
		excel =  xlrd.open_workbook('data/XLSs/' + lang + '.xls')

		#print excel

		for sheet_index in range(excel.nsheets):
			
			output_file = open('data/output/' + filelist[sheet_index] + '_' + lang + '.xml', 'w')

			sheet = excel.sheet_by_index(sheet_index)
			print sheet.name

			for row_index in range(sheet.nrows):
				if sheet.cell_value(row_index, 2) <> '':
					line = u'<string name="%(name)s">%(text)s</string>\n' % {
						'name':sheet.cell_value(row_index, 0), 
						'text':sheet.cell_value(row_index, 2)}
					output_file.write(line)

			output_file.close()
def handle_go_1():
	filelist = [u'OTA', u'便签', u'短信', u'计算器', u'联系人_', u'启动器', u'时钟']
	#filelist = ['OTA', '计算器', '时钟', '电话', '便签', '启动器', 'Framework', '锁屏', '设置', '相机&相册', '联系人_', '短信']
	langlist = ['zh-tw', 'kr']
	langtail = {'zh-tw':u' - 中文 - 表格 1', 'kr':u' - 中文 - 表格 1 - 表格 1'}

	for lang in langlist:
		print '====process language:' + lang

		# read excel
		excel =  xlrd.open_workbook('data/XLSs/' + lang + '.xls')

		for filename in filelist:
			print '====process file:' + filename
			# read xml
			xml = ET.parse('data/XMLs/' + filename + '.xml')
			strings = xml.findall('./string')

			#read sheet
			print filename + langtail[lang]
			sheet = excel.sheet_by_name(filename + langtail[lang])
			print 'rows:', sheet.nrows

			length = len(strings)
			sheet_index = 1

			for string_index in range(length):
				
				string_name = strings[string_index].attrib['name']
				sheet_name = sheet.cell(sheet_index, 0).value

				while string_name <> sheet_name:
					#print 'string_index:', string_index, '   sheet_index:', sheet_index
					#print strings[string_index].attrib['name']
					#print sheet.cell(sheet_index, 0).value
					string_index = string_index + 1
					if string_index >= length:
						break

					string_name = strings[string_index].attrib['name']
					sheet_name = sheet.cell(sheet_index, 0).value

				if string_index < length:
					#print 'string_index:', string_index, '   sheet_index:', sheet_index
					strings[string_index].text = repr(sheet.cell(sheet_index, 2).value)
					sheet_index = sheet_index + 1

				if sheet_index >= sheet.nrows:
					break

			xml.write('data/output/' + filename + '-' + lang + '.xml', 'utf-8')
def handle_test():
	filelist = [u'OTA', u'便签', u'短信', u'计算器', u'联系人', u'启动器', u'时钟']
	#filelist = ['OTA', '计算器', '时钟', '电话', '便签', '启动器', 'Framework', '锁屏', '设置', '相机&相册', '联系人_', '短信']
	langlist = ['zh-tw']

	for lang in langlist:
		print 'process language:' + lang
		# read excel
		excel =  xlrd.open_workbook('data/XLSs/' + lang + '.xls')

		for filename in filelist:
			print 'process file:' + filename

			# read xml
			xml = ET.parse('data/XMLs/' + filename + '.xml')
			strings = xml.findall('./string')

			print len(strings)

			#read sheet
			sheet = excel.sheet_by_name(filename + u' - 表格 1')
			print 'sheet is :' + sheet.name

			print excel.nsheets

			for i in range(7):
				print excel.sheets()[i].name
def handle_emoji():
    excel = xlwt.Workbook()

    sheet = excel.add_sheet('sheet1')
    count = 0

    path = '/users/liujiong/downloads/emoji'

    for item in os.listdir(path):
        if item <> '.DS_Store':
            sheet.write(count, 0, item)
            image_path = os.path.join(path, item)
            image = Image.open(image_path).convert('RGB')
            image.thumbnail((16,16), Image.ANTIALIAS )
            image.save(os.path.join('./image/', item + '.bmp'))
            sheet.insert_bitmap(os.path.join('./image/', item + '.bmp'), count, 1)
            count = count + 1

    excel.save('emoji.xls')

def handle_all_file():
	pass

def foo():
	print 'hello'

reload(sys) 
sys.setdefaultencoding( "utf-8" ) 
foo()