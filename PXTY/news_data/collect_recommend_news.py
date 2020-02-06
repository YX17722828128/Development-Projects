#!user/bin/env python3  
# -*- coding: utf-8 -*-
import requests
import re
from admin import setting

class Spider(object):
	"""docstring for spider"""
	def __init__(self):
		super(Spider, self).__init__()
		self.Iplist = []
		self.title_lsit = []
		self.link_list = []
		self.headers = {
		        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
		    }

	def getIP(self,pageno):
	    url = 'http://www.xicidaili.com/nn/' + str(pageno)
	    r = requests.get(url, timeout = 50, headers = self.headers)
	    r.encoding = r.apparent_encoding
	    html = r.text
	    plt = re.findall('<td>.*?</td>',html)
	    count = 1  
	    proxies = {}
	    _http = ''
	    _ip = ''
	    for data in plt:
	        initial_data = re.split('<td>|</td>',data)
	        completed_data = initial_data[1]
	        if count%5 == 1:
	            _ip = completed_data
	        elif count%5 == 3:
	            _http = completed_data
	        elif count%5 == 4 and ('分钟' not in completed_data):
	            proxies = {_http : _ip}  
	            self.Iplist.append(proxies)  
	        count += 1
	    return self.Iplist

	def judge(self,element):
			in_list = ["华为","移动","联通","电信"]
			out_list = ["百度","腾讯","阿里","中兴"]
			for i in range(4):
				if out_list[i] in element:
					return False
			for i in range(4):
				if in_list[i] in element:
					return True
			return False

	def part_1(self,list_no, proxies):
		url = "http://www.techweb.com.cn/mobile/list_" + str(list_no) + ".shtml"
		r = requests.get(url, timeout = 80, headers = self.headers, proxies = proxies)
		r.encoding = r.apparent_encoding
		html = r.text
		plt = re.findall(r'<div class="text">(.*?)</a>',html)
		for element in plt:
			if self.judge(element):
				title = re.findall(r'<h4>(.*?)</h4>', element)[0]
				link = re.findall(r'href="(.*?)"', element)[0]
				self.title_lsit.append(title)
				self.link_list.append(link)

	def part_2(self,proxies):
		url = "http://5g.zol.com.cn/"
		r = requests.get(url, timeout = 80, headers = self.headers, proxies = proxies)
		r.encoding = r.apparent_encoding
		html = r.text
		link_plt = re.findall(r'<a href="(.*?)" class="title" title=.*?</a>',html)
		title_plt = re.findall(r'<a href=".*?" class="title" title=(.*?)</a>',html)
		for i in range(len(title_plt)):
			title_plt[i] = title_plt[i].split(">")[1]
			if self.judge(title_plt[i]):
				self.title_lsit.append(title_plt[i])
				self.link_list.append(link_plt[i])

	def part_3(self,list_no, proxies):
		url = "http://www.huaweicloud.com/about/news_" + str(list_no) + ".html"
		r = requests.get(url, timeout = 80, headers = self.headers, proxies = proxies)
		r.encoding = r.apparent_encoding
		html = r.text
		link_plt = re.findall(r"<div class='new_text'><p><a href='(.*?)' target='_blank'>",html)
		title_plt = re.findall(r"<div class='new_text'><p><a href='.*?' target='_blank'>(.*?)</a></p>",html)
		for i in range(len(title_plt)):
			link_plt[i] = "http://www.huaweicloud.com" + link_plt[i]
			self.title_lsit.append(title_plt[i])
			self.link_list.append(link_plt[i])

	def insert_recommend_news(self):
		connection = setting()
		cursor = connection.cursor()
		cursor.execute(cursor.mogrify("TRUNCATE RECOMMEND_NEWS"))
		for i in range(len(self.title_lsit)):
			cursor.execute(cursor.mogrify("INSERT INTO RECOMMEND_NEWS(recommend_id, news_title, news_url) VALUES (%s, %s, %s)",(int(i+1), self.title_lsit[i], self.link_list[i])))
		connection.commit()
		cursor.close()
		connection.close()


def main():
	spider = Spider()
	for i in range(1,3):
		spider.getIP(i)

	for list_no in range(1,19):
		spider.part_1(list_no,spider.Iplist[list_no%len(spider.Iplist)])

	spider.part_2(spider.Iplist[list_no%len(spider.Iplist)])

	for list_no in range(1,6):
		spider.part_3(list_no,spider.Iplist[list_no%len(spider.Iplist)])

	spider.spider.insert_recommend_news()

if __name__ == '__main__':
	main()