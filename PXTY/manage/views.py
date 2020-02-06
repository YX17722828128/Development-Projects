#!user/bin/env python3  
# -*- coding: utf-8 -*-
from django.shortcuts import render
from functions.admin import setting
from django.http import HttpResponse,StreamingHttpResponse,JsonResponse,HttpResponseRedirect
# from django.views.decorators.cache import cache_page
# from django.core.cache import cache
from functions.establish_excel_form import get_excel_form
import os
import random,json
import requests,re
import time
import hashlib

appid = "xxx"
appsecret = "xxx"
# Create your views here.
def login_first(request):
	connection = setting()
	cursor = connection.cursor()
	xxx = request.GET["xxx"]
	request.session["xxx"] = xxx
	cursor.execute(cursor.mogrify("SELECT * FROM xxx WHERE xxx = %s",xxx))
	results = cursor.fetchone()
	cursor.close()
	connection.close()
	if results:
		return HttpResponse("sign in")
	else:
		return HttpResponse("sign up")

def sign_in(request):
	connection = setting()
	cursor = connection.cursor()
	xxx = request.GET["xxx"]
	xxx = request.session.get("xxx",default=None)
	cursor.execute(cursor.mogrify("SELECT * FROM xxx WHERE xxx = %s AND xxx = %s",(xxx,xxx)))
	results = cursor.fetchone()
	cursor.close()
	connection.close()
	if results:
		return HttpResponse("success")
	else:
		return HttpResponse("failure")

def sign_up(request):
	connection = setting()
	cursor = connection.cursor()
	xxx = request.GET["xxx"]
	xxx = request.session.get("xxx",default=None)
	cursor.execute(cursor.mogrify("INSERT INTO xxx(xxx, xxx) VALUES (%s, %s)",(account,xxx)))
	connection.commit()
	cursor.close()
	connection.close()
	return HttpResponse("success")

def carousel(request):
	connection = setting()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT xxx, xxx, xxx FROM xxx WHERE xxx = ANY(SELECT xxx FROM xxx)"))
	results = cursor.fetchall()
	cursor.close()
	connection.close()
	response_list = []
	for row in results:
		response_dict = {}
		response_dict["xxx"] = 1
		response_dict["xxx"] = row[0]
		response_dict["xxx"] = row[1]
		response_dict["xxx"] = row[2]
		response_list.append(response_dict)
	return JsonResponse(response_list, safe = False)

def news(request):
	connection = setting()
	cursor = connection.cursor()
	xxx = request.GET["xxx"]
	cursor.execute(cursor.mogrify("SELECT xxx, xxx, xxx, xxx, xxx, xxx, xxx, xxx FROM xxx WHERE xxx = %s"),int(xxx))
	results = cursor.fetchone()
	cursor.close()
	connection.close()
	response_dict = {}
	response_dict["xxx"] = results[0]
	response_dict["xxx"] = results[1]
	response_dict["xxx"] = results[2]
	response_dict["xxx"] = results[3]
	response_dict["xxx"] = results[4]
	response_dict["xxx"] = results[5]
	response_dict["xxx"] = results[6]
	response_dict["xxx"] = results[7]
	return JsonResponse(response_dict)

def upload_news(request):
	try:
		connection = setting()
		cursor = connection.cursor()
		cursor.execute(cursor.mogrify("SELECT MAX(xxx) FROM xxx"))
		result = cursor.fetchone()
		xxx = int(result[0]) + 1
		xxx = request.POST.get("xxx")
		xxx = request.FILES.get("xxx")
		xxx_path = os.getcwd()
		xxx_path = xxx_path.replace("\\","/")
		xxx_path = xxx_path + "/manage/templates/resource/news/" + xxx.name
		with open(xxx_path, "wb") as f:
			for i in xxx:
				f.write(i)
		xxx = request.POST.get("xxx")
		xxx = "background: url(\\\'resource/news/" + xxx.name + "\\\');" + xxx
		xxx = request.POST.get("xxx")
		xxx = request.POST.get("xxx")
		xxx = request.POST.get("xxx")
		xxx = request.POST.get("xxx")
		xxx = request.POST.get("xxx")
		cursor.execute(cursor.mogrify("INSERT INTO xxx(xxx, xxx, xxx, xxx, xxx, xxx, xxx, xxx) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(int(xxx), xxx, xxx, xxx, xxx, xxx, xxx, xxx)))
		connection.commit()
		cursor.close()
		connection.close()
		return HttpResponse("success")
	except Exception as e:
		return HttpResponse("failure")
	
def expense_application(request):
	try:
		connection = setting()
		cursor = connection.cursor()
		cursor.execute(cursor.mogrify("SELECT MAX(xxx) FROM xxx"))
		result = cursor.fetchone()
		xxx = int(result[0]) + 1
		xxx = request.session.get("account",default=None)
		xxx = time.strftime("%Y",time.localtime(time.time()))
		xxx,xxx,xxx,xxx = request.POST["xxx"],request.POST["xxx"],\
		request.POST["xxx"],request.POST["xxx"]
		xxx,xxx,xxx,xxx = request.POST["xxx"],request.POST["xxx"],\
		request.POST["xxx"],request.POST["xxx"]
		xxx = "checking"
		cursor.execute(cursor.mogrify("INSERT INTO xxx(xxx,xxx,xxx,xxx,xxx,xxx,xxx,\
		xxx,xxx,xxx,xxx,xxx) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" , \
		(int(expense_id),xxx,int(xxx),expense_date,xxx,xxx,xxx,xxx,float(xxx),\
			float(xxx),float(xxx),xxx)))
		connection.commit()
		cursor.close()
		connection.close()
		return HttpResponse("success")
	except Exception as e:
		return HttpResponse("failure")

def news_list(request):
	connection = setting()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT xxx, xxx FROM xxx WHERE xxx NOT IN (SELECT xxx FROM xxx)"))
	results = cursor.fetchall()
	cursor.close()
	connection.close()
	response_list = []
	for row in results:
		response_dict = {}
		response_dict["xxx"] = 0
		response_dict["xxx"] = row[0]
		response_dict["xxx"] = row[1]
		response_list.append(response_dict)
	return JsonResponse(response_list, safe = False)

def manage_carousel(request):
	try:
		connection = setting()
		cursor = connection.cursor()
		xxx = request.POST["xxx"]
		xxx = xxx.split(" ")
		while "" in xxx:
			xxx.remove("")
		sql = "TRUNCATE TABLE xxx"
		cursor.execute(sql)
		connection.commit()
		for data in xxx:
			cursor.execute(cursor.mogrify("INSERT INTO xxx(xxx) VALUES (%s)", int(data)))
			connection.commit()
		cursor.close()
		connection.close()
		return HttpResponse("success")
	except Exception as e:
		return HttpResponse("String format error")

def establish_form(request):
	connection = setting()
	cursor = connection.cursor()
	xxx = request.session.get("xxx",default=None)
	xxx = request.POST["xxx"]
	xxx = xxx.split(".")
	if len(xxx) == 1:
		cursor.execute(cursor.mogrify("SELECT xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx FROM xxx \
		WHERE xxx = %s AND xxx = %s  ORDER BY xxx", (xxx,int(xxx[0]))))
	elif len(xxx) == 2:
		cursor.execute(cursor.mogrify("SELECT xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx FROM xxx \
		WHERE xxx = %s AND xxx = %s AND xxx LIKE '%s.%%' ORDER BY xxx", (xxx,int(xxx[0]),int(xxx[1]))))
	insert_data = cursor.fetchall()
	cursor.close()
	connection.close()
	get_excel_form(insert_data,xxx,xxx)
	return HttpResponse("success")

def show_expense(request):
	xxx = request.session.get("xxx",default="")
	if xxx == "manager":
		def get_list(results):
			response_list = []
			for row in results:
				response_dict = {}
				response_dict["xxx"] = str(row[0])
				month, day = row[2].split(".")
				response_dict["xxx"] = str(row[1]) + "/" + month.zfill(2) + "/" + day.zfill(2)
				response_dict["xxx"] = row[3]
				response_dict["xxx"] = row[4]
				response_dict["xxx"] = row[5]
				response_dict["xxx"] = row[6]
				response_dict["xxx"] = row[7]
				response_dict["xxx"] = row[8]
				response_dict["xxx"] = row[9]
				response_dict["xxx"] = row[10]
				response_list.append(response_dict)
			return response_list
		connection = setting()
		cursor = connection.cursor()
		cursor.execute(cursor.mogrify("SELECT xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx FROM xxx \
		WHERE xxx = 'xxx' ORDER BY xxx DESC"))
		results = cursor.fetchall()
		xxx_part = get_list(results)
		cursor.execute(cursor.mogrify("SELECT xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx FROM xxx \
		WHERE xxx = 'xxx' ORDER BY xxx DESC"))
		results = cursor.fetchall()
		xxx_part = get_list(results)
		cursor.close()
		connection.close()
		response_data = {}
		response_data["xxx"] = xxx_part
		response_data["xxx"] = xxx_part
		return JsonResponse(response_data)
	else:
		return HttpResponse("you are not the manager")

def check_expense(request):
	xxx = request.session.get("xxx",default="")
	if xxx == "xxx":
		try:
			xxx = request.POST["xxx"]
			xxx = request.POST["xxx"]
			connection = setting()
			cursor = connection.cursor()
			cursor.execute(cursor.mogrify("UPDATE xxx SET xxx = %s WHERE xxx = %s", (xxx,int(xxx))))
			connection.commit()
			cursor.close()
			connection.close()
			return HttpResponse("success")
		except Exception as e:
			return HttpResponse("failure")
	else:
		return HttpResponse("lack of priority")

def download_form(request):
	file_name = "expense_claim_form.xlsx"
	def file_iterator(file_name, chunk_size=512):
		with open(file_name, "rb") as f:
			while True:
				c = f.read(chunk_size)
				if c:
					yield c
				else:
					break
	response = StreamingHttpResponse(file_iterator(file_name))
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
	return response

def recommend_news(request):
	connection = setting()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT MAX(xxx) FROM xxx"))
	result = cursor.fetchone()
	id_list = []
	for i in range(1,int(result[0])+1):
		id_list.append(i)
	xxx = random.sample(id_list,5) 
	cursor.execute(cursor.mogrify("SELECT * FROM xxx WHERE xxx in (%s, %s, %s, %s, %s)", (xxx[0], xxx[1], \
		xxx[2], xxx[3], xxx[4])))
	results = cursor.fetchall()
	cursor.close()
	connection.close()
	response_list = []
	for row in results:
		response_dict = {}
		response_dict["xxx"] = row[0]
		response_dict["xxx"] = row[1]
		response_dict["xxx"] = row[2]
		response_list.append(response_dict)
	return JsonResponse(response_list, safe = False)

# 头条部分
def part1_news_display(request):
	news_path = os.getcwd()
	news_path = news_path.replace("\\","/") + "/news_data/"
	news_file = os.listdir(news_path)
	response_list = []
	for i in range(8):
		fp = open(news_path+news_file[i],"r",encoding="utf-8") # news_file[i] == xxx.txt
		read_data = fp.read()
		read_data = eval(read_data)
		if i == 0:
			response_list.append({"news_id":news_file[i].split(".")[0],"news_title":read_data["news_title"],"news_content":read_data["news_content"]})
		else:
			response_list.append({"news_id":news_file[i].split(".")[0],"news_title":read_data["news_title"],"news_time":read_data["news_time"]})
		fp.close()
	return JsonResponse(response_list, safe = False)

# 观点部分
def part2_news_display(request):
	news_path = os.getcwd()
	news_path = news_path.replace("\\","/") + "/news_data/"
	news_file = os.listdir(news_path)
	response_list = []
	i = 8
	while i <= 14:
		fp = open(news_path+news_file[i],"r",encoding="utf-8") # news_file[i] == xxx.txt
		read_data = fp.read()
		read_data = eval(read_data)
		if "href" not in read_data["news_author"]:
			if ":" in read_data["news_author"]:
				author = read_data["news_author"].split(":",1)[1].split(" ",1)[0]
			elif "：" in read_data["news_author"]:
				author = read_data["news_author"].split("：",1)[1].split(" ",1)[0]		
			response_list.append({"news_id":news_file[i].split(".")[0],"news_title":read_data["news_title"],"news_author":author})
			i += 1
		fp.close()
	return JsonResponse(response_list, safe = False)

# 图片展示
def part3_news_display(request):
	news_path = os.getcwd()
	news_path = news_path.replace("\\","/") + "/news_data/"
	news_file = os.listdir(news_path)
	response_list = []
	select_list = [random.randint(0,len(news_file)) for _ in range(30)]
	i = 0
	for num in select_list:
		fp = open(news_path+str(num)+".txt","r",encoding="utf-8") # news_file[i] == xxx.txt
		read_data = fp.read()
		read_data = eval(read_data)
		if len(read_data["img_src_list"]) >= 1:
			response_list.append({"news_id":num,"news_title":read_data["news_title"],"img_src":read_data["img_src_list"][0]}) # 取第一张图片
			i += 1
			if i == 6:
				break
		fp.close()
	return JsonResponse(response_list, safe = False)

# 全部新闻
def part4_news_display(request):
	news_path = os.getcwd()
	news_path = news_path.replace("\\","/") + "/news_data/"
	news_file = os.listdir(news_path)
	response_list = []
	pageno = request.POST["pageno"]
	start_page = (int(pageno) - 1) * 7 + 1
	end_page = start_page + 8
	if start_page < len(news_file) and end_page > len(news_file):
		end_page = len(news_file)
	elif start_page > len(news_file):
		start_page, end_page = 0, 0
	for i in range(start_page,end_page):
		fp = open(news_path+str(i)+".txt","r",encoding="utf-8") # news_file[i] == xxx.txt
		read_data = fp.read()
		read_data = eval(read_data)
		if len(read_data["img_src_list"]) >= 1:
			response_list.append({"news_id":news_file[i].split(".")[0],"news_title":read_data["news_title"],"news_content":read_data["news_content"],\
				"news_time":read_data["news_time"],"img_src_list":read_data["img_src_list"][0]}) # 取第一张图片
		fp.close()
	return JsonResponse(response_list, safe = False)

def news_page_content(request):
	news_path = os.getcwd()
	news_path = news_path.replace("\\","/") + "/news_data/"
	news_id = request.POST["news_id"]
	fp = open(news_path+str(news_id)+".txt","r",encoding="utf-8")
	read_data = fp.read()
	read_data = eval(read_data)
	response_dict = {}
	response_dict["news_id"] = news_id
	response_dict["news_title"] = read_data["news_title"]
	response_dict["news_time"] = read_data["news_time"]
	response_dict["news_author"] = read_data["news_author"]
	response_dict["news_content"] = read_data["news_content"]
	response_dict["img_src_list"] = read_data["img_src_list"]
	return JsonResponse(response_dict)

def test(request):
	return render(request, "test.html")

def locate_file(request):
	file_root = "C:/Users/Administrator/Desktop/PXTY/manage/templates/"
	if request.get_full_path()[len(request.get_full_path())-1] != '/':
		file_path = request.get_full_path()[1:len(request.get_full_path())]
	else:
		file_path = request.get_full_path()[1:len(request.get_full_path())-1]
	if file_path[len(file_path)-3:len(file_path)] == "png" or file_path[len(file_path)-3:len(file_path)] == "jpg" or file_path[len(file_path)-4:len(file_path)] == "jpeg":
		image_data = open(file_root+file_path,"rb").read()
		return HttpResponse(image_data,content_type="image/jpeg")
	elif file_path[len(file_path)-3:len(file_path)] == "css":
		css_data = open(file_root+file_path,"rb").read()
		return HttpResponse(css_data,content_type="text/css")
	else:
		return render(request, file_path)
	# return render(request, "test.html")


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

def test_file(request):
	bg_img = request.FILES.get("file")
	bg_img_path = os.getcwd()
	bg_img_path = bg_img_path.replace("\\","/")
	bg_img_path = bg_img_path + "/" + bg_img.name
	with open(bg_img_path, "wb") as f:
		for i in bg_img:
			f.write(i)
	return HttpResponse("success")

def start_login(request):
	redirect_uri = "http://szpxty.cn/confirm_login/"
	href = "https://open.weixin.qq.com/connect/oauth2/authorize?appid="+appid+"&redirect_uri="+redirect_uri+"&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
	return HttpResponseRedirect(href)

def confirm_login(request):
	url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid="+appid+"&secret="+appsecret+"&code="+request.GET['code']+"&grant_type=authorization_code"
	r = requests.get(url)
	r.encoding = r.apparent_encoding
	JSON = r.text
	JSON = eval(JSON) # JSON['access_token'],JSON['expires_in'],JSON['refresh_token'],JSON['openid'],JSON['scope']

	## 获取用户详细信息 ###
	url = "https://api.weixin.qq.com/sns/userinfo?access_token=" + JSON['access_token'] + "&openid=" + JSON['openid'] + "&lang=zh_CN"
	r = requests.get(url)
	r.encoding = r.apparent_encoding
	JSON = r.text
	JSON = eval(JSON) # openid,nickname,sex,province,city,country,headimgurl,privilege,unionid
	request.session["openid"] = JSON['openid']
	connection = setting()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT openid FROM xxx WHERE openid = %s", JSON['openid']))
	result = cursor.fetchone()
	if result:
		cursor.execute(cursor.mogrify("REPLACE INTO xxx(openid,nickname,sex,province,city,country,headimgurl) VALUES (%s,%s,%s,%s,%s,%s,%s)", \
			(JSON['openid'],JSON['nickname'],JSON['sex'],JSON['province'],JSON['city'],JSON['country'],JSON['headimgurl'])))	
		connection.commit()
		cursor.close()
		connection.close()
		redirect_uri = "http://szpxty.cn/"
		return HttpResponseRedirect(redirect_uri)
	else:
		cursor.close()
		connection.close()
		return HttpResponse("failure")

def get_jsapi_ticket():
	url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+appid+'&secret='+appsecret
	r = requests.get(url)
	r.encoding = r.apparent_encoding
	html = eval(r.text)
	access_token = html["access_token"]
	ticket_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token='+access_token+'&type=jsapi'
	r = requests.get(ticket_url)
	r.encoding = r.apparent_encoding
	html = eval(r.text)
	jsapi_ticket = html["ticket"]
	return jsapi_ticket

def jssdk_config(request):
	connection = setting()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT xxx FROM xxx"))
	result = cursor.fetchone()
	if result:
		xxx = "xxx=" + result[0]
	else:
		xxx = get_xxx()
		cursor.execute(cursor.mogrify("INSERT INTO xxx(xxx) VALUES (%s)", (xxx)))
		connection.commit()
		xxx = "xxx=" + xxx
	cursor.close()
	connection.close()
	
	Token = "py_access"
	nonceStr = "noncestr=" + Token
	stamp = str(int(time.time()))
	timestamp = "timestamp=" + stamp
	url = "url=" + request.GET["url_str"]

	hashlist = [xxx, nonceStr, timestamp, url]
	hashlist.sort()
	hashstr = '&'.join([s for s in hashlist])
	signature = hashlib.sha1(hashstr.encode("utf8")).hexdigest()
	data = {}
	data["appId"],data["timestamp"],data["nonceStr"] = appid,stamp,Token
	data["signature"],data["jsApiList"] = signature,["onMenuShareTimeline","onMenuShareAppMessage",\
	"onMenuShareQQ","onMenuShareWeibo","onMenuShareQZone","getLocation"]
	return JsonResponse(data)

def get_location(request):
	latitude = request.POST['latitude']
	longitude = request.POST['longitude']
	headers = {
			        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
			    }
	url = 'https://apis.map.qq.com/jsapi?qt=rgeoc&lnglat='+longitude+'%2C'+latitude+'&key=FBOBZ-VODWU-C7SVF-B2BDI-UK3JE-YBFUS&output=jsonp&pf=jsapi&ref=jsapi&cb=qq.maps._svcb3.geocoder0'
	r = requests.get(url, headers = headers)
	html = r.text
	province = re.findall(r'\"p\":\"(.*?)\"', html)[0]
	city = re.findall(r'\"c\":\"(.*?)\"', html)[0]
	district = re.findall(r'\"d\":\"(.*?)\"', html)[0]
	xxx = province + city + district
	xxx = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
	xxx = request.session.get('xxx',default=None)
	connection = setting()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("INSERT INTO xxx(xxx,xxx,xxx) VALUES (%s,%s,%s)", (xxx,xxx,xxx)))
	connection.commit()
	cursor.close()
	connection.close()
	return HttpResponse(xxx)

def location_history(request):
	xxx = request.session.get('xxx',default=None)
	connection = setting()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT xxx,xxx FROM xxx WHERE xxx = %s", (xxx)))
	results = cursor.fetchall()
	cursor.close()
	connection.close()
	response_list = []
	for row in results:
		response_dict = {}
		response_dict['xxx'] = row[0]
		response_dict['xxx'] = row[1]
		response_list.append(response_dict)
	return JsonResponse(response_list, safe = False)

def user_data(request):
	xxx = request.session.get('xxx',default=None)
	connection = setting()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT xxx,xxx,xxx,xxx,xxx,xxx,xxx FROM xxx WHERE xxx = %s", xxx))
	results = cursor.fetchone()
	cursor.close()
	connection.close()
	response_dict = {}
	response_dict['xxx'] = results[0]
	response_dict['xxx'] = results[1]
	if results[2] == '1':
		response_dict['xxx'] = '男'
	else:
		response_dict['sex'] = '女'
	response_dict['xxx'] = results[3]
	response_dict['xxx'] = results[4]
	response_dict['xxx'] = results[5]
	response_dict['xxx'] = results[6]
	return JsonResponse(response_dict)