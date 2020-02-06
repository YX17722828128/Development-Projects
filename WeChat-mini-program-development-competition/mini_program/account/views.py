from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.utils.html import escape
from django.core.cache import cache
from account.admin import connect
import time
import re
import requests
from bs4 import BeautifulSoup

# Create your views here.
def test(request):
	request.session["wx_id"] = "kjudmo8hssl7aaa"
	return render(request,"test.html")

def first_login(request):
	js_code = request.GET["code"]
	url = "https://api.weixin.qq.com/sns/jscode2session?appid=wx4334ea5bd2b5b82e&secret=33348cbcb4701c18a1a74e9c27068aab&js_code="+js_code+"&grant_type=authorization_code"
	r = requests.get(url)
	r.encoding = r.apparent_encoding
	html = eval(r.text)
	openid = html["openid"]
	session_key = html["session_key"]
	try:
		unionid = html["unionid"]
	except:
		unionid = "null"
	connection = connect()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("INSERT INTO xxx(openid,session_key,unionid) VALUES (%s,%s,%s)", (openid,session_key,unionid)))
	connection.commit()
	cursor.close()
	connection.close()
	return HttpResponse(openid)

def login(request):
	wx_id = request.GET["id"]
	wx_name = request.GET["name"]
	wx_sex = request.GET["sex"]
	wx_headimgurl = request.GET["headimgurl"]
	connection = connect()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("REPLACE INTO xxx(wx_id,wx_name,wx_sex,wx_headimgurl) VALUES (%s,%s,%s,%s)",(wx_id,wx_name,wx_sex,wx_headimgurl)))
	connection.commit()
	cursor.close()
	connection.close()
	return HttpResponse("success")

def add_account_book(request):
	wx_id = request.GET["wx_id"]
	account_book_name = escape(request.GET["book_name"])
	total_balance = float(escape(request.GET["total_balance"]))
	connection = connect()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT account_book_name FROM xxx WHERE wx_id = %s AND account_book_name = %s", (wx_id,account_book_name)))
	if cursor.fetchone():
		cursor.close()
		connection.close()
		return HttpResponse("failure")
	else:
		localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		timestamp = int(time.mktime(time.strptime(localtime, "%Y-%m-%d %H:%M:%S")))
		account_book_id = wx_id + "_book_" + str(timestamp)
		cursor.execute(cursor.mogrify("INSERT INTO xxx(wx_id,account_book_id,account_book_name,total_balance) VALUES (%s,%s,%s,%s)",(wx_id,account_book_id,account_book_name,total_balance)))
		connection.commit()
		cursor.close()
		connection.close()
		return HttpResponse(account_book_id)

def delete_account_book(request):
	account_book_id = escape(request.GET["account_book_id"])
	connection = connect()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT account_book_id FROM xxx WHERE account_book_id = %s", account_book_id))
	delete_book_id = cursor.fetchone()
	if delete_book_id:
		cursor.execute(cursor.mogrify("DELETE FROM xxx WHERE account_book_id = %s", delete_book_id[0]))
		connection.commit()
		cursor.close()
		connection.close()
		return HttpResponse("success")
	else:
		cursor.close()
		connection.close()
		return HttpResponse("failure")

def add_type(request):
	wx_id = request.GET["wx_id"]
	status = escape(request.GET["status"])
	status = int(status)
	if status == 1:
		type_status = "支出"
	else:
		type_status = "收入"
	localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
	timestamp = int(time.mktime(time.strptime(localtime, "%Y-%m-%d %H:%M:%S")))
	type_id = wx_id + "_type_" + str(timestamp)
	type_name = escape(request.GET["type_name"])
	connection = connect()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT type_name FROM xxx WHERE wx_id = %s AND type_status = %s AND type_name = %s", (wx_id,type_status,type_name)))
	if cursor.fetchone():
		cursor.close()
		connection.close()
		return HttpResponse("failure")
	else:
		cursor.execute(cursor.mogrify("INSERT INTO xxx(wx_id,type_id,type_status,type_name) VALUES (%s,%s,%s,%s)", (wx_id,type_id,type_status,type_name)))
		connection.commit()
		cursor.close()
		connection.close()
		return HttpResponse(type_id)

def delete_type(request):
	type_id = escape(request.GET["type_id"])
	connection = connect()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT type_name FROM xxx WHERE type_id = %s", type_id))
	if cursor.fetchone():
		cursor.execute(cursor.mogrify("DELETE FROM xxx WHERE type_id = %s", type_id))
		connection.commit()
		cursor.execute(cursor.mogrify("UPDATE xxx SET type_id = %s WHERE type_id = %s", ("null",type_id)))
		connection.commit()
		cursor.close()
		connection.close()
		return HttpResponse("success")
	else:
		cursor.close()
		connection.close()
		return HttpResponse("failure")

def add_balance_record(request):
	wx_id = request.GET["wx_id"]
	type_id = escape(request.GET["type_id"])
	status = int(escape(request.GET["status"]))
	if status == 1:
		type_status = "支出"
	else:
		type_status = "收入"
	balance_value = float(escape(request.GET["value"]))
	balance_date = escape(request.GET["date"])
	balance_description = escape(request.GET["description"])
	localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
	timestamp = int(time.mktime(time.strptime(localtime, "%Y-%m-%d %H:%M:%S")))
	balance_id = wx_id + "_balance_" + str(timestamp)
	connection = connect()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("INSERT INTO xxx(type_id,type_status,balance_id,balance_value,balance_date,balance_description) \
	 VALUES (%s,%s,%s,%s,%s,%s)", (type_id,type_status,balance_id,balance_value,balance_date,balance_description)))
	connection.commit()
	cursor.close()
	connection.close()
	return HttpResponse(balance_id)

def delete_balance_record(request):
	balance_id = escape(request.GET["balance_id"])
	connection = connect()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("DELETE FROM xxx WHERE balance_id = %s", balance_id))
	connection.commit()
	cursor.close()
	connection.close()
	return HttpResponse("success")

def show_balance(request):
	wx_id = request.GET["wx_id"]
	balance_date = escape(request.GET["date"])
	status = int(escape(request.GET["status"]))
	type_id = escape(request.GET["type_id"])
	connection = connect()
	cursor = connection.cursor()
	if balance_date == "*":
		if type_id == "*":
			if status == 0:
				cursor.execute(cursor.mogrify("SELECT SUM(balance_value) FROM xxx WHERE type_id LIKE %s AND type_status = %s", (wx_id+"%","收入")))
				IN = cursor.fetchone()
				IN = IN[0]
				if IN == None:
					IN = 0
				cursor.execute(cursor.mogrify("SELECT SUM(balance_value) FROM xxx WHERE type_id LIKE %s AND type_status = %s", (wx_id+"%","支出")))
				OUT = cursor.fetchone()
				OUT = OUT[0]
				if OUT == None:
					OUT = 0
				result = ("%.2f" % (IN-OUT))
				result = float(result)
				cursor.close()
				connection.close()
				return JsonResponse({"result":result}) # 总结余
			else:
				if status == 1:
					cursor.execute(cursor.mogrify("SELECT balance_id,type_status,balance_value,balance_date,balance_description FROM xxx \
						WHERE type_id LIKE %s AND type_status = %s", (wx_id+"%","支出")))
				elif status == 2:
					cursor.execute(cursor.mogrify("SELECT balance_id,type_status,balance_value,balance_date,balance_description FROM xxx \
						WHERE type_id LIKE %s AND type_status = %s", (wx_id+"%","收入")))
				results = cursor.fetchall()
				response_list = []
				for row in results:
					response_dict = {}
					response_dict["balance_id"] = row[0]
					response_dict["type_status"] = row[1]
					response_dict["balance_value"] = row[2]
					response_dict["balance_date"] = row[3]
					response_dict["balance_description"] = row[4]
					response_list.append(response_dict)
				cursor.close()
				connection.close()
				return JsonResponse(response_list, safe = False) # 总收入 || 总支出
		else:
			cursor.execute(cursor.mogrify("SELECT balance_id,type_status,balance_value,balance_date,balance_description FROM xxx \
					WHERE type_id = %s", type_id))
			results = cursor.fetchall()
			response_list = []
			for row in results:
				response_dict = {}
				response_dict["balance_id"] = row[0]
				response_dict["type_status"] = row[1]
				response_dict["balance_value"] = row[2]
				response_dict["balance_date"] = row[3]
				response_dict["balance_description"] = row[4]
				response_list.append(response_dict)
			cursor.close()
			connection.close()
			return JsonResponse(response_list, safe = False) # 某类型总收入 || 某类型总支出
	else:
		if type_id == "*":
			if status == 0:
				cursor.execute(cursor.mogrify("SELECT SUM(balance_value) FROM xxx WHERE type_id LIKE %s AND type_status = %s \
					AND balance_date LIKE %s", (wx_id+"%","收入",balance_date+"%")))
				IN = cursor.fetchone()
				IN = IN[0]
				if IN == None:
					IN = 0
				cursor.execute(cursor.mogrify("SELECT SUM(balance_value) FROM xxx WHERE type_id LIKE %s AND type_status = %s \
					AND balance_date LIKE %s", (wx_id+"%","支出",balance_date+"%")))
				OUT = cursor.fetchone()
				OUT = OUT[0]
				if OUT == None:
					OUT = 0
				result = ("%.2f" % (IN-OUT))
				result = float(result)
				cursor.close()
				connection.close()
				return JsonResponse({"result":result}) # （日/月/年）结余
			else:
				if status == 1:
					cursor.execute(cursor.mogrify("SELECT balance_id,type_status,balance_value,balance_date,balance_description FROM xxx \
						WHERE type_id LIKE %s AND type_status = %s AND balance_date LIKE %s", (wx_id+"%","支出",balance_date+"%")))
				elif status == 2:
					cursor.execute(cursor.mogrify("SELECT balance_id,type_status,balance_value,balance_date,balance_description FROM xxx \
						WHERE type_id LIKE %s AND type_status = %s AND balance_date LIKE %s", (wx_id+"%","收入",balance_date+"%")))
				results = cursor.fetchall()
				response_list = []
				for row in results:
					response_dict = {}
					response_dict["balance_id"] = row[0]
					response_dict["type_status"] = row[1]
					response_dict["balance_value"] = row[2]
					response_dict["balance_date"] = row[3]
					response_dict["balance_description"] = row[4]
					response_list.append(response_dict)
				cursor.close()
				connection.close()
				return JsonResponse(response_list, safe = False) # （日/月/年）收入 || （日/月/年）支出
		else:
			cursor.execute(cursor.mogrify("SELECT balance_id,type_status,balance_value,balance_date,balance_description FROM xxx \
					WHERE type_id = %s AND balance_date LIKE %s", (type_id,balance_date+"%")))
			results = cursor.fetchall()
			response_list = []
			for row in results:
				response_dict = {}
				response_dict["balance_id"] = row[0]
				response_dict["type_status"] = row[1]
				response_dict["balance_value"] = row[2]
				response_dict["balance_date"] = row[3]
				response_dict["balance_description"] = row[4]
				response_list.append(response_dict)
			cursor.close()
			connection.close()
			return JsonResponse(response_list, safe = False) # （日/月/年）某类型收入 || （日/月/年）某类型支出

def get_account_books(request):
	wx_id = request.GET["wx_id"]
	connection = connect()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT account_book_id,account_book_name,total_balance FROM xxx WHERE wx_id = %s", wx_id))
	results = cursor.fetchall()
	response_list = []
	for row in results:
		response_dict = {}
		response_dict["account_book_id"] = row[0]
		response_dict["account_book_name"] = row[1]
		response_dict["total_balance"] = row[2]
		response_list.append(response_dict)
	cursor.close()
	connection.close()
	return JsonResponse(response_list, safe = False)

def get_account_types(request):
	wx_id = request.GET["wx_id"]
	connection = connect()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT type_id,type_status,type_name FROM xxx \
		WHERE wx_id = %s", wx_id))
	results = cursor.fetchall()
	response_list = []
	for row in results:
		response_dict = {}
		response_dict["type_id"] = row[0]
		response_dict["type_status"] = row[1]
		response_dict["type_name"] = row[2]
		response_list.append(response_dict)
	cursor.close()
	connection.close()
	return JsonResponse(response_list, safe = False)

def handle_book(request):
	wx_id = request.GET["wx_id"]
	account_book_id = escape(request.GET["account_book_id"])
	change_value = float(escape(request.GET["change_value"]))
	connection = connect()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT total_balance FROM xxx WHERE wx_id = %s AND account_book_id = %s", (wx_id,account_book_id)))
	result = cursor.fetchone()
	result = float(result[0])
	cursor.execute(cursor.mogrify("UPDATE xxx SET total_balance = %s WHERE account_book_id = %s", (result-change_value,account_book_id)))
	connection.commit()
	cursor.execute(cursor.mogrify("INSERT INTO xxx(wx_id,account_book_id,change_value) VALUES (%s,%s,%s)", (wx_id,account_book_id,change_value)))
	connection.commit()
	cursor.close()
	connection.close()
	return HttpResponse("success")

def book_transfer(request):
	wx_id = request.GET["wx_id"]
	account_book_id_1 = escape(request.GET["account_book_id_1"])
	transfer_value = float(escape(request.GET["transfer_value"]))
	account_book_id_2 = escape(request.GET["account_book_id_2"])
	connection = connect()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify("SELECT total_balance FROM xxx WHERE wx_id = %s AND account_book_id = %s", (wx_id,account_book_id_1)))
	result = cursor.fetchone()
	result = float(result[0])
	cursor.execute(cursor.mogrify("UPDATE xxx SET total_balance = %s WHERE wx_id = %s AND account_book_id = %s", (result-transfer_value,wx_id,account_book_id_1)))
	connection.commit()
	cursor.execute(cursor.mogrify("SELECT total_balance FROM xxx WHERE wx_id = %s AND account_book_id = %s", (wx_id,account_book_id_2)))
	result = cursor.fetchone()
	result = float(result[0])
	cursor.execute(cursor.mogrify("UPDATE xxx SET total_balance = %s WHERE wx_id = %s AND account_book_id = %s", (result+transfer_value,wx_id,account_book_id_2)))
	connection.commit()
	cursor.execute(cursor.mogrify("INSERT INTO xxx(wx_id,account_book_id,change_value) VALUES (%s,%s,%s)", (wx_id,account_book_id_1,-transfer_value)))
	connection.commit()
	cursor.execute(cursor.mogrify("INSERT INTO xxx(wx_id,account_book_id,change_value) VALUES (%s,%s,%s)", (wx_id,account_book_id_2,transfer_value)))
	connection.commit()
	connection.close()
	cursor.close()
	return HttpResponse("success")

def exchange_rate(request):
	rate_dict = cache.get("exchange_rate") 
	if rate_dict == None:
		headers = {
				        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
				    }
		r = requests.get("http://hl.anseo.cn/", timeout = 50, headers = headers)
		r.encoding = r.apparent_encoding
		html = r.text
		soup = BeautifulSoup(html,"html.parser")
		links = soup.find_all("li", class_ = ["ev","od"])
		test_rule_1 = r" 人民币 = \d{1,12}.\d{1,12}"
		test_rule_2 = r" = \d{1,12}.\d{1,12} 人民币"
		rate_dict = {}
		for link in links:
			text = str(link.text)
			if re.search(test_rule_1, text):
				curreny = re.findall(r"[^()]+", text)[1]
				rate = re.findall(r"(\d+\.\d+)", text)[0]
				rate_dict["RMB-"+str(curreny)] = float(rate)
			elif re.search(test_rule_2, text):
				curreny = re.findall(r"[^()]+", text)[1]
				rate = re.findall(r"(\d+\.\d+)", text)[0]
				rate_dict[str(curreny)+"-RMB"] = float(rate)
		cache.set("exchange_rate", rate_dict, 1800)
		rate_dict = cache.get("exchange_rate") 
	currency1 = escape(request.GET["currency1"])
	currency2 = escape(request.GET["currency2"])
	rate = rate_dict[currency1+"-"+currency2]
	return HttpResponse(rate)

def mp4_file(request):
	return render(request, "video_test.html")