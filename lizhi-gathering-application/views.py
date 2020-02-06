from admin import db2,main_url
from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse,JsonResponse,HttpResponseRedirect
from django.utils.html import escape
import time

# Create your views here.
def EditBasicUserInfo(request):
	WxId = request.POST['WxId']
	CampusCardNo = escape(request.POST['CampusCardNo'])
	RealName = escape(request.POST['RealName']) # make sure all data had been input in the frontend
	connection = db2()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify('REPLACE INTO basic_user_info(WxId,CampusCardNo,RealName) VALUES (%s,%s,%s)',\
	 (WxId,CampusCardNo,RealName)))
	connection.commit()
	cursor.execute(cursor.mogrify('SELECT WxId FROM xxx WHERE WxId = %s', WxId))
	result = cursor.fetchone()
	cursor.close()
	connection.close()
	if result == None:
		return HttpResponse('fill in more') # jump to page for more detail(first login)
	return HttpResponse('completed')

def EditDetailUserInfo(request):
	WxId = request.POST['WxId']
	UserName = escape(request.POST['UserName'])
	Gender = escape(request.POST['Gender'])
	College = escape(request.POST['College'])
	Grade = escape(request.POST['Grade']) # make sure all data had been input in the frontend
	connection = db2()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify('REPLACE INTO xxx(WxId,UserName,Gender,College,Grade) VALUES (%s,%s,%s,%s,%s)',\
	 (WxId,UserName,Gender,College,Grade)))
	connection.commit()
	cursor.close()
	connection.close()
	return HttpResponse('success')

def PublishGathering(request):
	WxId = request.POST['WxId']
	PublishTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
	TimeStamp = int(time.mktime(time.strptime(PublishTime, "%Y-%m-%d %H:%M:%S")))
	GroupId = WxId+'@'+str(TimeStamp)
	GroupName = escape(request.POST['GroupName'])
	GroupSynopsis = escape(request.POST['GroupSynopsis'])
	TargetMemberNo = int(escape(request.POST['TargetMemberNo']))
	PresentMemberNo = 0
	DeadLine = escape(request.POST['DeadLine']) # the format is Y-M-D H:M:S, frontend should firstly check foramt
	GroupImage = escape(request.POST['GroupImage'])
	PresentState = 'visible'
	ContactInfo = escape(request.POST['ContactInfo'])
	ParticipationState = 'participating'
	Identity = 'manager'
	connection = db2()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify('INSERT INTO xxx(GroupId,GroupName,GroupSynopsis,TargetMemberNo,PresentMemberNo,DeadLine,GroupImage,PresentState,PublishTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',\
	 (GroupId,GroupName,GroupSynopsis,TargetMemberNo,PresentMemberNo,DeadLine,GroupImage,PresentState,PublishTime)))
	connection.commit()
	cursor.execute(cursor.mogrify('INSERT INTO xxx(WxId,GroupId,ParticipationState,ContactInfo,Identity) VALUES (%s,%s,%s,%s,%s)',\
	 (WxId,GroupId,ParticipationState,ContactInfo,Identity)))
	connection.commit()
	cursor.close()
	connection.close()
	return HttpResponse('success')

def RevokeGathering(request):
	WxId = request.POST['WxId']
	GroupId = request.POST['GroupId']
	connection = db2()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify('SELECT Identity FROM xxx WHERE WxId = %s AND GroupId = %s', (WxId,GroupId)))
	Identity = cursor.fetchone()
	if Identity[0] == 'manager':
		cursor.execute(cursor.mogrify('SELECT PresentState FROM xxx WHERE GroupId = %s', (GroupId)))
		PresentState = cursor.fetchone()
		if PresentState[0] == 'visible':
			cursor.execute(cursor.mogrify('UPDATE xxx SET PresentState = %s WHERE GroupId = %s', ('invisible',GroupId)))
			connection.commit()
			cursor.close()
			connection.close()
			return HttpResponse('success')
		else:
			cursor.close()
			connection.close()
			return HttpResponse('had revoked')
	else:
		cursor.close()
		connection.close()
		return HttpResponse('failure')

def PublishGroupNotice(request):
	WxId = request.POST['WxId']
	GroupId = request.POST['GroupId']
	connection = db2()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify('SELECT Identity FROM xxx WHERE WxId = %s AND GroupId = %s', (WxId,GroupId)))
	Identity = cursor.fetchone()
	if Identity[0] == 'manager':
		GroupNotice = escape(request.POST['GroupNotice'])
		cursor.execute(cursor.mogrify('UPDATE xxx SET GroupNotice = %s WHERE GroupId = %s', (GroupNotice,GroupId)))
		connection.commit()
		cursor.close()
		connection.close()
		return HttpResponse('success')
	else:
		cursor.close()
		connection.close()
		return HttpResponse('failure')

def ReEditGathering(request):
	WxId = request.POST['WxId']
	GroupId = request.POST['GroupId']
	PublishTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
	connection = db2()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify('SELECT Identity FROM xxx WHERE WxId = %s AND GroupId = %s', (WxId,GroupId)))
	Identity = cursor.fetchone()
	if Identity[0] == 'manager':
		cursor.execute(cursor.mogrify('SELECT PresentState FROM xxx WHERE GroupId = %s', (GroupId)))
		PresentState = cursor.fetchone()
		if PresentState[0] == 'visible':
			cursor.close()
			connection.close()
			return HttpResponse('revoke first')
		else:
			# frontend should make sure TargetMemberNo >= PresentMemberNo
			# what frontend transfer to here are GroupSynopsis,TargetMemberNo,DeadLine,GroupImage
			GroupSynopsis,TargetMemberNo = escape(request.POST['GroupSynopsis']),escape(request.POST['TargetMemberNo'])
			DeadLine,GroupImage = escape(request.POST['DeadLine']),escape(request.POST['GroupImage'])
			cursor.execute(cursor.mogrify('UPDATE xxx SET GroupSynopsis = %s, TargetMemberNo = %s, DeadLine = %s, GroupImage = %s, PresentState = %s, PublishTime = %s \
				WHERE GroupId = %s', (GroupSynopsis,TargetMemberNo,DeadLine,GroupImage,'visible',PublishTime,GroupId)))
			connection.commit()
			cursor.close()
			connection.close()
			return HttpResponse('success')
	else:
		cursor.close()
		connection.close()
		return HttpResponse('failure')

def JoinGroup(request):
	WxId = request.POST['WxId']
	GroupId = request.POST['GroupId']
	ParticipationState = 'participating'
	ContactInfo = escape(request.POST['ContactInfo'])
	Identity = 'member'
	connection = db2()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify('SELECT TargetMemberNo,PresentMemberNo FROM xxx WHERE GroupId = %s', (GroupId)))
	result = cursor.fetchone()
	TargetMemberNo,PresentMemberNo = int(result[0]),int(result[1])
	if PresentMemberNo+1 > TargetMemberNo:
		cursor.close()
		connection.close()
		return HttpResponse('failure')
	else:
		cursor.execute(cursor.mogrify('INSERT INTO xxx(WxId,GroupId,ParticipationState,ContactInfo,Identity) VALUES (%s,%s,%s,%s,%s)',\
		 (WxId,GroupId,ParticipationState,ContactInfo,Identity)))
		connection.commit()
		cursor.execute(cursor.mogrify('UPDATE xxx SET PresentMemberNo = PresentMemberNo+1 WHERE GroupId = %s', (GroupId)))
		connection.commit()
		cursor.close()
		connection.close()
		return HttpResponse('success')

def LeftGroup(request):
	WxId = request.POST['WxId']
	GroupId = request.POST['GroupId']
	connection = db2()
	cursor = connection.cursor()
	cursor.execute(cursor.mogrify('SELECT Identity FROM xxx WHERE WxId = %s AND GroupId = %s', (WxId,GroupId)))
	Identity = cursor.fetchone()
	if Identity[0] == 'manager':
		cursor.close()
		connection.close()
		return HttpResponse('failure')
	else:
		cursor.execute(cursor.mogrify('UPDATE xxx SET ParticipationState = %s WHERE WxId = %s AND GroupId = %s', ('withdrawn',WxId,GroupId)))
		connection.commit()
		cursor.execute(cursor.mogrify('UPDATE xxx SET PresentMemberNo = PresentMemberNo-1 WHERE GroupId = %s', (GroupId)))
		connection.commit()
		cursor.close()
		connection.close()
		return HttpResponse('success')

def test(request):
	return render(request, 'test.html')