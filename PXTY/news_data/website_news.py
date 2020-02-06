#!user/bin/env python3  
# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

Iplist = []
ip_count = 0
headers = {
		        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
		    }
matches = ['华为', '海思', '寒武纪', '中国移动', '中国联通', '中国电信', '沃达丰', '亚马逊', '谷歌', '安卓', '微软', '5G', '4G', '信息化', '数字化', '数字时代', '云', '大数据', 'AI', '人工智能', '智慧城市', '平安城市', '电子政务', '数字铁路', '数字城轨', '智慧', '自动驾驶', '互联网', '网络', '物联网', 'IoT', '电信', '通信', '运营商', '手机', '任正非', '孙亚芳', '余承东', '尚冰', '苗圩', '台积电', '北斗', '区块链']
unmatches = ['高通', '思科', '中兴', '侯为贵', '联想', '柳传志', '杨元庆', '惠普', '戴尔', 'OPPO', 'VIVO', '小米', '雷军', '金立', '魅族', '三星', '苹果', '库克', '罗永浩', '阿里巴巴', '马云', '腾讯', '马化腾', '淘宝', '京东', '百度', '坚果', '锤子', '一加', 'MIX']
NEWS_DATA = {}
NEWS_ID = 1
def getIP(pageno):
	global Iplist,ip_count,headers,matches,unmatches,NEWS_DATA,NEWS_ID
	url = 'http://www.xicidaili.com/nn/' + str(pageno)
	r = requests.get(url, timeout = 30, headers = headers)
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
			Iplist.append(proxies)  
		count += 1


def collect(number, url, raw_sub_test, raw_target_test, title_rule, time_rule, source_rule, author_rule, content_rule, delete_img_1, outlink_rule):
	global Iplist,ip_count,headers,matches,unmatches,NEWS_DATA,NEWS_ID
	r = requests.get(url, timeout = 50, headers = headers, proxies = Iplist[ip_count%len(Iplist)])
	ip_count += 1
	r.encoding = r.apparent_encoding
	html = r.text
	soup = BeautifulSoup(html,"html.parser")
	links = soup.find_all("a")
	sub_link = []
	target_link = []
	for link in links:
		if any(data in str(link) for data in matches)==True and any(data in str(link) for data in unmatches)==False:
			sub_test = re.search(raw_sub_test, str(link["href"]))
			target_test = re.search(raw_target_test, str(link["href"]))
			if sub_test and str(link["href"]) not in sub_link:
				sub_link.append(str(link["href"]))
			elif target_test and str(link["href"]) not in target_link:
				target_link.append(str(link["href"]))
	for data in sub_link:
		if len(target_link) >= number:
			break
		if data[0:4] != "http":
			if url == "https://www.huxiu.com/":
				r = requests.get("https://www.huxiu.com"+data, timeout = 50, headers = headers, proxies = Iplist[ip_count%len(Iplist)])
			elif url == "http://www.tmtpost.com/":
				r = requests.get("http://www.tmtpost.com"+data+".html", timeout = 50, headers = headers, proxies = Iplist[ip_count%len(Iplist)])
			else:
				r = requests.get("http:"+data, timeout = 50, headers = headers, proxies = Iplist[ip_count%len(Iplist)])
		else:
			r = requests.get(data, timeout = 50, headers = headers, proxies = Iplist[ip_count%len(Iplist)])
		ip_count += 1
		r.encoding = r.apparent_encoding
		html = r.text
		soup = BeautifulSoup(html,"html.parser")
		links = soup.find_all("a")
		for link in links:
			if len(target_link) >= number:
				break
			try:
				sub_test = re.search(raw_sub_test,str(link["href"]))
				target_test = re.search(raw_target_test,str(link["href"]))
				if target_test and str(link["href"]) not in target_link:
					target_link.append(str(link["href"]))
				elif any(data in str(link) for data in matches)==True and any(data in str(link) for data in unmatches)==False:			
					if sub_test and str(link["href"]) not in sub_link:
						sub_link.append(str(link["href"]))
			except:
				continue

	for target in target_link:
		news_data = {}
		if target[0:4] != "http":
			if url == "https://www.huxiu.com/":
				r = requests.get("https://www.huxiu.com"+target, timeout = 50, headers = headers, proxies = Iplist[ip_count%len(Iplist)])
			elif url == "http://www.tmtpost.com/":
				r = requests.get("http://www.tmtpost.com"+target, timeout = 50, headers = headers, proxies = Iplist[ip_count%len(Iplist)])
			else:
				r = requests.get("http:"+target, timeout = 50, headers = headers, proxies = Iplist[ip_count%len(Iplist)])
		else:
			r = requests.get(target, timeout = 50, headers = headers, proxies = Iplist[ip_count%len(Iplist)])
		ip_count += 1
		if url == "http://www.tmtpost.com/":
			r.encoding = "utf-8"
		else:
			r.encoding = r.apparent_encoding
		html = r.text
		soup = BeautifulSoup(html,"html.parser")

		if url == "https://www.huxiu.com/":
			news_url = "https://www.huxiu.com" + target
		elif url == "http://www.tmtpost.com/":
			news_url = "http://www.tmtpost.com" + target
		else:
			news_url = target

		try:
			news_title = soup.find_all(title_rule)
			news_title = str(news_title[0].get_text())

			if any(data in news_title for data in unmatches)==True:
				pass

			if time_rule[0] == "id":
				news_time = soup.find(time_rule[1], id=time_rule[2])
			elif time_rule[0] == "class":
				news_time = soup.find(time_rule[1], class_=time_rule[2])
			news_time = str(news_time.get_text())

			if url == "https://www.huxiu.com/":
				news_source = "虎嗅网"
			elif url == "http://www.tmtpost.com/":
				news_source = "钛媒体"
			else:
				if source_rule[0] == "id":
					news_source = soup.find(source_rule[1], id=source_rule[2])
				elif source_rule[0] == "class":
					news_source = soup.find(source_rule[1], class_=source_rule[2])
				news_source = str(news_source.get_text())
				news_source = news_source.replace("\xa0","")

			if url == "http://tech.ifeng.com/":
				news_author = "凤凰网"
			elif url == "http://tech.caijing.com.cn/":
				news_author = "钛极客"
			else:
				if author_rule[0] == "id":
					news_author = soup.find(author_rule[1], id=author_rule[2])
				elif author_rule[0] == "class":
					news_author = soup.find(author_rule[1], class_=author_rule[2])
				news_author = str(news_author.get_text())

			if url == "http://www.tmtpost.com/":
				news_content = soup.find("article")
			else:
				if content_rule[0] == "id":
					news_content = soup.find(content_rule[1], id=content_rule[2])
				elif content_rule[0] == "class":
					news_content = soup.find(content_rule[1], class_=content_rule[2])
			news_content = str(news_content)
			news_content = news_content.replace("\xa0","")
		except:
			continue

		if delete_img_1:
			try:
				first_img_start = news_content.index("<img")
				end_img_start = news_content.find(">",first_img_start)+1
				news_content = news_content.replace(news_content[first_img_start:end_img_start],"")
			except:
				pass

		try:
			first_outlink_start = news_content.index(outlink_rule[0])
			end_outlink_start = news_content.find(outlink_rule[1],first_outlink_start)+4
			news_content = news_content.replace(news_content[first_outlink_start:end_outlink_start],"")
		except:
			pass

		try:
			content_soup = BeautifulSoup(news_content,"html.parser")
		except:
			continue	

		# news_content = []
		news_content = {"text":"", "img":""}
		if url == "https://www.huxiu.com/":
			start_img = soup.find("div", class_="article-img-box")
			start_img = start_img.find("img")
			start_img = str(start_img["src"])
			# news_content.append({"text":"","img":start_img})
			news_content["img"] = start_img
		paragraphs = content_soup.find_all("p")
		news_content["text"] = paragraphs[0].get_text()
		if news_content["img"] == "":
			for p in paragraphs:
				if "<img" in str(p):
					try:
						img = p.find("img")
						img = str(img["src"])
						news_content["img"] = img
					except:
						news_content["img"] = ""
		# for p in paragraphs:
		# 	paragraphs_json = {}
		# 	paragraphs_json["text"] = p.get_text()
		# 	if "<img" in str(p):
		# 		try:
		# 			img = p.find("img")
		# 			img = str(img["src"])
		# 			paragraphs_json["img"] = img
		# 		except:
		# 			paragraphs_json["img"] = ""
		# 	news_content.append(paragraphs_json)
		news_data["news_url"], news_data["news_title"], news_data["news_time"]= news_url, news_title, news_time
		news_data["news_source"], news_data["news_author"], news_data["news_content"]= news_source, news_author, news_content
		NEWS_DATA[NEWS_ID] = news_data
		NEWS_ID += 1

def write_data():
	f = open("today_news.txt", "w", encoding="utf-8")
	f.write(str(NEWS_DATA))
	f.close()

def main(factor):
	for i in range(1,7):
		getIP(i)

	url = "http://www.zol.com.cn"
	raw_sub_test = r'^http://(.*?).zol.com.cn/$'
	raw_target_test = r'^http://(.*?).zol.com.cn/689/\d{1,12}.html$'
	title_rule = "h1"
	time_rule = ["id", "span", "pubtime_baidu"]
	source_rule = ["id", "span", "source_baidu"]
	author_rule = ["id", "span", "author_baidu"]
	content_rule = ["class", "div", "article-cont clearfix"]
	delete_img_1 = True
	outlink_rule = ["<p class=\"crawl-none", "</p>"]
	collect(factor, url, raw_sub_test, raw_target_test, title_rule, time_rule, source_rule, author_rule, content_rule, delete_img_1, outlink_rule)

	url = "http://www.pconline.com.cn/"
	raw_sub_test = r'^//(.*?).pconline.com.cn/$'
	raw_target_test = r'^//(.*?).pconline.com.cn/1124/\d{1,12}.html$'
	title_rule = "h1"
	time_rule = ["class", "span", "pubtime"]
	source_rule = ["class", "span", "source"]
	author_rule = ["class", "span", "author"]
	content_rule = ["class", "div", "content"]
	delete_img_1 = False
	outlink_rule = ["<p class=\"crawl-none", "</p>"]
	collect(factor, url, raw_sub_test, raw_target_test, title_rule, time_rule, source_rule, author_rule, content_rule, delete_img_1, outlink_rule)

	url = "https://www.huxiu.com/"
	raw_sub_test = r'^/channel/\d{1,12}.html$'
	raw_target_test = r'^/article/\d{1,12}.html$'
	title_rule = "h1"
	time_rule = ["class", "span", "article-time"]
	source_rule = ["class", "span", "source"]
	author_rule = ["class", "span", "author-name"]
	content_rule = ["class", "div", "article-content-wrap"]
	delete_img_1 = False
	outlink_rule = ["<p class=\"crawl-none", "</p>"]
	collect(factor, url, raw_sub_test, raw_target_test, title_rule, time_rule, source_rule, author_rule, content_rule, delete_img_1, outlink_rule)

	url = "http://www.tmtpost.com/"
	raw_sub_test = r'^/column/\d{1,12}$'
	raw_target_test = r'^/\d{1,12}.html$'
	title_rule = "h1"
	time_rule = ["class", "span", "time"]
	source_rule = ["class", "span", "source"]
	author_rule = ["class", "a", "color-orange"]
	content_rule = ["class", "div", "article"]
	delete_img_1 = False
	outlink_rule = ["<p class=\"crawl-none", "</p>"]
	collect(factor, url, raw_sub_test, raw_target_test, title_rule, time_rule, source_rule, author_rule, content_rule, delete_img_1, outlink_rule)

	url = "http://tech.ifeng.com/"
	raw_sub_test = r'^http://(.*?).ifeng.com/$'
	raw_target_test = r'^http://(.*?).ifeng.com/a/\d{1,12}/\d{1,12}_0.shtml$'
	title_rule = "h1"
	time_rule = ["class", "span", "ss01"]
	source_rule = ["class", "span", "ss03"]
	author_rule = ["id", "span", "author_baidu"]
	content_rule = ["id", "div", "main_content"]
	delete_img_1 = False
	outlink_rule = ["<p class=\"crawl-none", "</p>"]
	collect(factor, url, raw_sub_test, raw_target_test, title_rule, time_rule, source_rule, author_rule, content_rule, delete_img_1, outlink_rule)

	url = "http://tech.caijing.com.cn/"
	raw_sub_test = r'^http://(.*?).caijing.com.cn/$'
	raw_target_test = r'^http://(.*?).caijing.com.cn/\d{1,12}/\d{1,12}.shtml$'
	title_rule = "h2"
	time_rule = ["class", "span", "news_time"]
	source_rule = ["class", "span", "news_name"]
	author_rule = ["id", "span", "author_baidu"]
	content_rule = ["class", "div", "article-content"]
	delete_img_1 = False
	outlink_rule = ["<p class=\"crawl-none", "</p>"]
	collect(factor, url, raw_sub_test, raw_target_test, title_rule, time_rule, source_rule, author_rule, content_rule, delete_img_1, outlink_rule)

	write_data()

if __name__ == '__main__':
	factor = 2
	main(factor) # the number of news will be factor * 6