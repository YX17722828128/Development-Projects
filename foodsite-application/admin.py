import pymysql

DATABASE_1 = {
        'HOST': '55c5f3742f54d.gz.cdb.myqcloud.com',
        'USER': 'xxx',        
        'PASSWORD': 'xxx',    
        'NAME': 'yongxin',  
        'PORT': '13125',
}
def db():
    db = pymysql.connect(DATABASE_1["HOST"],DATABASE_1["USER"],DATABASE_1["PASSWORD"],DATABASE_1["NAME"],int(DATABASE_1["PORT"]),charset="utf8")
    return db


DATABASE_2 = {
        'HOST': '127.0.0.1',
        'USER': 'xxx',        
        'PASSWORD': 'xxx',    
        'NAME': 'gathering',  
        'PORT': '3306',
}
def db2():
    db2 = pymysql.connect(DATABASE_2["HOST"],DATABASE_2["USER"],DATABASE_2["PASSWORD"],DATABASE_2["NAME"],int(DATABASE_2["PORT"]),charset="utf8")
    return db2


VAR = {
		'appid': 'xxx', 
		'appsecret': 'xxx',
		'token': 'xxx',
		'hone_url': 'www.niyong.xin', # 填写主域名，如lizhi.szer.me, 不用加http(s)
}
def variables():
	return VAR["appid"],VAR["appsecret"],VAR["token"]

def main_url():
	return VAR["hone_url"]