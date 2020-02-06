from django.shortcuts import render
from admin import db,main_url
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.html import escape
import jieba
import json
import requests
import re
from bs4 import BeautifulSoup
import hashlib
import time

def get(request):
	#下面这四个参数是在接入时，微信的服务器发送过来的参数
	signature = request.GET.get('signature', None)
	timestamp = request.GET.get('timestamp', None)
	nonce = request.GET.get('nonce', None)
	echostr = request.GET.get('echostr', None)
	#这个token是自己定义的，填写在开发文档中的Token的位置
	token = 'py_access'
	#把token，timestamp, nonce放在一个序列中，并且按字符排序
	hashlist = [token, timestamp, nonce]
	hashlist.sort()
	#将上面的序列合成一个字符串
	hashstr = ''.join([s for s in hashlist])
	#通过python标准库中的sha1加密算法，处理上面的字符串，形成新的字符串。
	hashstr = hashlib.sha1(hashstr.encode("utf8")).hexdigest()
	#把生成的字符串和微信服务器发送过来的字符串比较，
	#如果相同，就把服务器发过来的echostr字符串返回去
	if hashstr == signature:
		return HttpResponse(echostr)
	

def redirect(request):
	return render(request, 'redirect.html')

def get_jsapi_ticket():
	SIGN = time.strftime("%Y-%m-%d")
	MD5 = hashlib.md5()
	MD5.update(SIGN.encode(encoding='utf-8'))
	MD5 = MD5.hexdigest()
	SIGN = hashlib.sha1(MD5.encode("utf8")).hexdigest()
	url = "http://lizhi.szer.me/proxy/forward.php?sign="+SIGN+"&action=WjJWMFYzaEJkWFJvUVdOalpYTnpWRzlyWlc0PQ"
	r = requests.get(url)
	r.encoding = r.apparent_encoding
	html = eval(r.text)
	access_token = html["access_token"]
	ticket_url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token="+access_token+"&type=jsapi"
	r = requests.get(ticket_url)
	r.encoding = r.apparent_encoding
	html = eval(r.text)
	jsapi_ticket = html["ticket"]
	return jsapi_ticket

def auto_share_config(request):
	connection = db()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT jsapi_ticket FROM xxx"))
	result = cursor.fetchone()
	if result:
		jsapi_ticket = "jsapi_ticket=" + result[0]
	else:
		jsapi_ticket = get_jsapi_ticket()
		cursor.execute(cursor.mogrify("INSERT INTO xxx(jsapi_ticket) VALUES (%s)", (jsapi_ticket)))
		connection.commit()
		jsapi_ticket = "jsapi_ticket=" + jsapi_ticket
	cursor.close()
	connection.close()
	
	Token = "py_access"
	nonceStr = "noncestr=" + Token
	stamp = str(int(time.time()))
	timestamp = "timestamp=" + stamp
	url = "url=" + request.GET["url_str"]

	hashlist = [jsapi_ticket, nonceStr, timestamp, url]
	hashlist.sort()
	hashstr = '&'.join([s for s in hashlist])
	signature = hashlib.sha1(hashstr.encode("utf8")).hexdigest()
	data = {}
	data["appId"],data["timestamp"],data["nonceStr"] = "wxde6a9e2fd63767d5",stamp,Token
	data["signature"],data["jsApiList"] = signature,["onMenuShareTimeline","onMenuShareAppMessage",\
	"onMenuShareQQ","onMenuShareWeibo","onMenuShareQZone"]
	return JsonResponse(data)
	

@cache_page(60 * 30)
def home(request):
	try:
		'''
		SIGN = time.strftime("%Y-%m-%d")
		MD5 = hashlib.md5()
		MD5.update(SIGN.encode(encoding='utf-8'))
		MD5 = MD5.hexdigest()
		SIGN = hashlib.sha1(MD5.encode("utf8")).hexdigest()
		url = "http://lizhi.szer.me/proxy/forward.php?sign="+SIGN+"&action=WjJWMFYzaEJZMk5sYzNOVWIydGxiZz09"
		postdata = {'code':request.GET['code']}
		r = requests.post(url,data=postdata)
		r.encoding = r.apparent_encoding
		JSON = r.text
		JSON = eval(JSON)
		# print(JSON['access_token'],JSON['expires_in'],JSON['refresh_token'],JSON['openid'],JSON['scope'])
		connection = db()
		cursor = connection.cursor()
		cursor.execute(cursor.mogrify("DELETE FROM user WHERE openid = %s", JSON['openid']))
		connection.commit()

		SIGN = "py_access" + JSON['openid']
		MD5 = hashlib.md5()
		MD5.update(SIGN.encode(encoding='utf-8'))
		MD5 = MD5.hexdigest()
		secret_id = hashlib.sha1(MD5.encode("utf8")).hexdigest()

		cursor.execute(cursor.mogrify("INSERT INTO user(access_token,expires_in,refresh_token,openid,secret_id) VALUES (%s,%s,%s,%s,%s)", (JSON['access_token'],int(JSON['expires_in']),JSON['refresh_token'],JSON['openid'],secret_id)))
		connection.commit()
		cursor.close()
		connection.close()
		'''
		request.session["secret_id"] = 'xxx'
		request.session["openid"] = 'xxx'
		### 获取用户详细信息 ###
		# url = "https://api.weixin.qq.com/sns/userinfo?access_token=" + JSON['access_token'] + "&openid=" + JSON['openid'] + "&lang=zh_CN"
		# r = requests.get(url)
		# r.encoding = r.apparent_encoding
		# JSON = r.text
		# JSON = eval(JSON)
		# print(JSON['openid'],JSON['nickname'],JSON['sex'],JSON['language'],JSON['city'],JSON['province'],JSON['province'],JSON['country'],JSON['headimgurl'],JSON['privilege'])
		if request.session.get("first_search_content",default=None) != None:
			first_search_content = request.session.get("first_search_content",default=None)
			request.session["first_search_content"] = None
			return HttpResponseRedirect("http://www.niyong.xin/lib/storage_book/?search_content="+first_search_content)
		if request.session.get("first_detail_content",default=None) != None:
			first_detail_content = request.session.get("first_detail_content",default=None)
			request.session["first_detail_content"] = None
			return HttpResponseRedirect("http://www.niyong.xin/lib/book_detail/?ctrlno="+str(first_detail_content))
		return render(request, 'home.html', {'secret_id':'xxx'})
	except Exception as e:
		return render(request, 'redirect.html')
	

def template(request):
	search_id = request.GET['search_id']
	secret_id = request.GET['secret_id']
	if secret_id == "null":
		'''
		SIGN = "py_access" + request.session.get("openid",default=None)
		MD5 = hashlib.md5()
		MD5.update(SIGN.encode(encoding='utf-8'))
		MD5 = MD5.hexdigest()
		secret_id = hashlib.sha1(MD5.encode("utf8")).hexdigest()
		'''
		secret_id = 'xxx'
	connection = db()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("DELETE FROM xxx WHERE secret_id = %s", secret_id))
	connection.commit()
	cursor.execute(cursor.mogrify("INSERT INTO xxx(secret_id,stu_no) VALUES (%s,%s)", (secret_id,search_id)))
	connection.commit()
	cursor.close()
	connection.close()
	return HttpResponse(secret_id)


@cache_page(60 * 15)
def return_book(request):
	List_for_data = []
	inner_list = []
	student_id = request.GET['student_id']
	student_id = str(student_id)
	try:
		connection = db()
		cursor = connection.cursor()
		cursor.execute(cursor.mogrify("SELECT return_date,request_no,name_author FROM xxx WHERE STUDENT_ID = %s", student_id))
		results = cursor.fetchall()
		cursor.close()
		connection.close()
		results = list(results)		
		if results:
			for row in results:
				N_A = str(row[2])
				N_A = N_A.split("／")
				inner_list.append("书名: ")
				inner_list.append(N_A[0])
				inner_list.append("作者: ")
				inner_list.append(N_A[1])
				inner_list.append("索取号: ")
				inner_list.append(str(row[1]))
				inner_list.append("应还日期: ")
				inner_list.append(str(row[0]))
				List_for_data.append(inner_list)
				inner_list = []			
		else:
			inner_list.append("result empty!")
			List_for_data.append(inner_list)
			inner_list = []
	except Exception as e:
		inner_list.append("Error: unable to fetch data")
		List_for_data.append(inner_list)
		inner_list = []
	return render(request, 'return_book_info.html', {'data_array':List_for_data})
	

def get_all_books(search_content):
	sorted_result = []
	key_words = []
	temp = search_content
	search_content = re.sub("[\.\!\/_,$%^*(\"\')]|[—()?【】“”！，。？、~@#￥%……&*（）]", "",search_content)
	if len(search_content) > 0:
		connection = db()
		cursor = connection.cursor()
		if len(search_content) < 4 or re.match('^[0-9a-zA-Z]+$',search_content):
			cursor.execute(cursor.mogrify("SELECT name,author,pub_house,pub_year,ctrlno FROM xxx WHERE name LIKE %s ORDER BY ctrlno", "%" + search_content + "%"))
			results = cursor.fetchall()
			sorted_result = list(results)
			key_words.append(search_content)
			if not sorted_result:
				cursor.execute(cursor.mogrify("SELECT name,author,pub_house,pub_year,ctrlno FROM xxx WHERE author LIKE %s ORDER BY ctrlno", "%" + search_content + "%"))
				results = cursor.fetchall()
				sorted_result.extend(list(results)) 
		else:
			pro_string = jieba.cut(search_content)
			seg_string = ",".join(pro_string)
			seg_list = seg_string.split(",")
			while " " in seg_list:
				seg_list.remove(" ")
			seg_length = len(seg_list)
			if seg_length == 1:
				key_words = seg_list
				cursor.execute(cursor.mogrify("SELECT name,author,pub_house,pub_year,ctrlno FROM xxx WHERE name LIKE %s ORDER BY ctrlno", "%" + seg_list[0] + "%"))
				results = cursor.fetchall()
				sorted_result = list(results)
				if not sorted_result:
					cursor.execute(cursor.mogrify("SELECT name,author,pub_house,pub_year,ctrlno FROM xxx WHERE author LIKE %s ORDER BY ctrlno", "%" + seg_list[0] + "%"))
					results = cursor.fetchall()
				if results:
					sorted_result.extend(list(results)) 
			elif seg_length == 2:
				key_words = seg_list
				cursor.execute(cursor.mogrify("SELECT name,author,pub_house,pub_year,ctrlno FROM xxx WHERE name LIKE %s AND name LIKE %s ORDER BY ctrlno", ("%" + seg_list[0] + "%","%" + seg_list[1] + "%")))
				results = cursor.fetchall()
				sorted_result = list(results)
				cursor.execute(cursor.mogrify("SELECT name,author,pub_house,pub_year,ctrlno FROM xxx WHERE author LIKE %s AND author LIKE %s ORDER BY ctrlno", ("%" + seg_list[0] + "%","%" + seg_list[1] + "%")))
				results = cursor.fetchall()
				if results:
					sorted_result.extend(list(results)) 
			elif seg_length > 2:
				key_words = seg_list[0:3]
				cursor.execute(cursor.mogrify("SELECT name,author,pub_house,pub_year,ctrlno FROM xxx WHERE name LIKE %s AND name LIKE %s AND name LIKE %s ORDER BY ctrlno", ("%" + seg_list[0] + "%","%" + seg_list[1] + "%","%" + seg_list[2] + "%")))
				results = cursor.fetchall()
				sorted_result = list(results)
				cursor.execute(cursor.mogrify("SELECT name,author,pub_house,pub_year,ctrlno FROM xxx WHERE author LIKE %s AND name LIKE %s AND author LIKE %s ORDER BY ctrlno", ("%" + seg_list[0] + "%","%" + seg_list[1] + "%","%" + seg_list[2] + "%")))
				results = cursor.fetchall()
				if results:
					sorted_result.extend(list(results)) 
		cursor.close()
		connection.close()
		for i in range(len(sorted_result)):
			if str(sorted_result[i][0]) == temp:
				sorted_result.insert(0, sorted_result[i])
				del sorted_result[i+1]
				
		return sorted_result,key_words
	else:
		return ["NULL"],["error_info"]
	

def get_book_list(search_content,status,pageno = 1):
	pageno = int(pageno)
	List_for_data = []
	inner_list = []
	if cache.get("sorted_result","nothing") == "nothing" or cache.get("sorted_result","-----") != search_content\
	    or status == "retype":
		sorted_result, key_words = get_all_books(search_content)
		cache.set("sorted_result",sorted_result)
		cache.set("key_words",key_words)
		cache.set("search_content",search_content)
	else:
		sorted_result, key_words = cache.get("sorted_result","nothing"), cache.get("key_words","nothing")
	if sorted_result:
		count = 0
		begin_count = (pageno-1)*15
		end_count = (pageno)*15
		for row in sorted_result:
			if count>=begin_count and count < end_count:
				inner_list.append(str(row[0])) # 书名
				inner_list.append(str(row[1])) # 作者
				inner_list.append(str(row[2])) # 出版社
				inner_list.append(str(row[3])) # 出版日期
				inner_list.append(str(row[4])) # ctrlno
				List_for_data.append(inner_list)
				inner_list = []		
			if count > end_count:
				break
			count += 1
	else:
		inner_list.append("result empty!")
		List_for_data.append(inner_list)
		inner_list = []
		key_words = ['≮']
	return List_for_data, key_words


def storage_book(request,pageno = 1):
	secret_id = request.session.get("secret_id",default="null")
	openid = request.session.get("openid",default="SID@"+secret_id)
	if secret_id == "null":
		secret_id = 'xxx'
	if secret_id == "null":
		request.session["first_search_content"] = request.GET['search_content']
		href = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxde6a9e2fd63767d5&redirect_uri=http%3A%2F%2Flizhi.szer.me%2Fproxy%2Fcode.php&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
		return HttpResponseRedirect(href)
	else:
		search_content = request.GET['search_content']
		search_content = escape(search_content)
		last_content = request.session.get("search_content",default=None)
		request.session["search_content"] = search_content
		agent = request.META.get('HTTP_USER_AGENT')
		try:
			ip =  request.META['HTTP_X_REAL_IP']
		except Exception as e:
			if 'HTTP_X_FORWARDED_FOR' in request.META:  
			    ip =  request.META['HTTP_X_FORWARDED_FOR']  
			else:  
			    ip = request.META['REMOTE_ADDR'] 
		connection = db()
		cursor = connection.cursor()
		cursor.execute(cursor.mogrify("INSERT INTO xxx(openid,agent,ip,search_time,search_content) VALUES (%s,%s,%s,now(),%s)", (openid,agent,ip,search_content)))
		connection.commit()
		cursor.close()
		connection.close()
		back_search_content = []
		back_search_content.append(search_content)
		List_for_data = []
		key_words = []
		List_for_data, key_words = get_book_list(search_content,"retype",pageno)
		return render(request, 'storage_book_info.html',{'data_array':List_for_data, 'key_words':key_words, 'search_content':back_search_content})
	

@cache_page(60 * 15)
def book_detail(request):
	secret_id = request.session.get("secret_id",default="null")
	if secret_id == "null":
		secret_id = 'xxx'
	if secret_id == "null":
		request.session["first_detail_content"] = request.GET['ctrlno']
		href = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxde6a9e2fd63767d5&redirect_uri=http%3A%2F%2Flizhi.szer.me%2Fproxy%2Fcode.php&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
		return HttpResponseRedirect(href)
	else:
		ctrlno = request.GET['ctrlno']
		List_for_data = []
		list_info = []
		List_for_data, list_info, name, author, house = get_book_status(ctrlno)
		return render(request, 'book_detail_info.html', {'List_for_data':List_for_data, 'list_info':list_info, 'name':name, 'author':author, 'house':house})
	

def get_book_status(ctrlno):
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
	url = 'http://opac.lib.szu.edu.cn/opac/bookinfo.aspx?ctrlno=' + ctrlno
	connection = db()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT ip FROM xxx ORDER BY rand() LIMIT 1"))
	PROXIES = cursor.fetchall()
	proxies_list = re.findall("\"(.*?)\"",str(PROXIES))
	cursor.close()
	connection.close()
	r = requests.get(url, timeout = 30, headers = headers, proxies = eval(proxies_list[0]))
	r.encoding = r.apparent_encoding
	html = r.text
	html = r.text
	soup = BeautifulSoup(html, "html.parser")
	pub_summary = ""
	try:
		try:
			pub_summary = soup.find_all(id="ctl00_ContentPlaceHolder1_bookcardinfolbl")[0]
			pub_summary = re.findall("<br/><br/>(.*?)<br/><br/>", str(pub_summary))[0]
			pub_summary = pub_summary.replace("\u3000", "")
		except Exception as e:
			pub_summary = " "

		tbhead = soup.find_all(class_="tbhead")[0]
		tbhead = re.findall("<td.*?>(.*?)</td>", str(tbhead))

		addr = []
		request_no = []
		status = []
		tbody = soup.find_all("tbody")[0]
		tbody_soup = BeautifulSoup(str(tbody), "html.parser")
		tbody_list = tbody_soup.select("td")
		for i in range(0,len(tbody_list)):
			try:
				tbody_list[i] = str(re.findall("<td>(.*?)</td>",str(tbody_list[i]),re.S|re.M)[0])
				if "href" in tbody_list[i]:
					addr_detail = ""
					addr_data = re.findall(">(.*?)<",tbody_list[i],re.S|re.M)
					for data in addr_data:
						addr_detail += data
					tbody_list[i] = addr_detail
				if "\r\n" in tbody_list[i]:
					tbody_list[i] = tbody_list[i].replace("\r\n","")
					tbody_list[i] = tbody_list[i].strip()
			except Exception as e:
				tbody_list[i] = " "
		if len(tbhead) == 7:
			for i in range(0,len(tbody_list)):
				if i%7 == 0:
					addr.append(tbody_list[i])
				elif i%7 == 1:
					request_no.append(tbody_list[i])
				elif i%7 == 5:
					status.append(tbody_list[i])
		elif len(tbhead) == 8:
			for i in range(0,len(tbody_list)):
				if i%8 == 0:
					addr.append(tbody_list[i])
				elif i%8 == 2:
					request_no.append(tbody_list[i])
				elif i%8 == 6:
					status.append(tbody_list[i])

		if "href" in pub_summary:
			pub_summary = "信息暂无"
			status = ['仅供阅览','仅供阅览','仅供阅览','仅供阅览']

		list_info = []
		inner_list_info = []
		for i in range(len(addr)):
			inner_list_info.append("馆藏地：" + addr[i])
			inner_list_info.append("索取号：" + request_no[i])
			inner_list_info.append("状态：" + status[i])
			list_info.append(inner_list_info)
			inner_list_info = []

		book_number = len(addr)
		borrow_number = 0
		for data in status:
			if "借" in data:
				borrow_number += 1
		List_for_data = []
		inner_list = []
		name = ""
		author = ""
		house = ""
		try:
			connection = db()
			cursor = connection.cursor()
			cursor.execute(cursor.mogrify("SELECT * FROM xxx WHERE CTRLNO = %s", int(ctrlno)))
			results = cursor.fetchall()
			cursor.close()
			connection.close()
			results = list(results)		
			temp_count = 0
			if results:
				for row in results:
					inner_list.append("《" + row[1] + "》")
					name = row[1]
					inner_list.append("馆藏: " + str(book_number))
					inner_list.append("可借: " + str(borrow_number))
					inner_list.append("作者: " + row[2])
					author = row[2]
					inner_list.append("出版社: " + row[3])
					house = row[3]
					inner_list.append("出版日期: " + row[4])
					pub_summary = pub_summary.replace("<br/>","")
					inner_list.append("摘要: " + pub_summary)
					List_for_data.append(inner_list)
					inner_list = []			
					temp_count += 1
					if temp_count == 1:
						break
			else:
				inner_list.append("result empty!")
				List_for_data.append(inner_list)
				inner_list = []
		except Exception as e:
			inner_list.append("Error: unable to fetch data")
			List_for_data.append(inner_list)
			inner_list = []

	except Exception as e:
		raise e

	return List_for_data, list_info, name, author, house
	

def ajax_storage_book(request):
	pageno = request.GET['pageno']
	List_for_data = []
	key_words = []
	search_content = request.session.get("search_content",default=None)
	List_for_data, key_words = get_book_list(search_content,"ajax",pageno)
	List_for_data.insert(0, key_words)
	return HttpResponse(json.dumps(List_for_data), content_type='application/json')
	

def wx_redirect(request):
	secret_id = request.GET['secret_id']
	if secret_id == "null":		
		href = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxde6a9e2fd63767d5&redirect_uri=http%3A%2F%2Flizhi.szer.me%2Fproxy%2Fcode.php&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
		return HttpResponseRedirect(href)
	else:
		request.session["secret_id"] = secret_id
		return render(request, 'home.html', {'secret_id':secret_id})