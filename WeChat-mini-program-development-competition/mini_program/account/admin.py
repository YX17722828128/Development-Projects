import pymysql

DATABASES = {
        'HOST': '127.0.0.1',
        'USER': 'account_admin',        
        'PASSWORD': 'account_admin',    
        'NAME': 'account',  
        'PORT': '3306',
}
def connect():
	db = pymysql.connect(DATABASES["HOST"],DATABASES["USER"],DATABASES["PASSWORD"],DATABASES["NAME"],int(DATABASES["PORT"]),charset="utf8")
	return db