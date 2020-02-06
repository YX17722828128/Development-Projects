from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse,JsonResponse
from food_site.models import *
import datetime
from django.utils.html import escape
import urllib.parse

# Create your views here.
def dish(request):
	restaurant_id = escape(request.POST["restaurant_id"])
	data = getDishes(restaurant_id)
	return JsonResponse(data, safe = False)

def order(request):
	user_id = escape(request.POST["user_id"])
	data = getOrderForms(user_id)
	return JsonResponse(data, safe = False)

def get_comments(request):
	dish_id = escape(request.POST["dish_id"])
	data = getComments(dish_id)
	return JsonResponse(data, safe = False)

def search_dishes(request):
	words = escape(request.POST["words"])
	data = searchDishes(words)
	return JsonResponse(data, safe = False)

def write_comments(request):
	user_id=escape(request.POST["user_id"])
	dish_id=escape(request.POST["dish_id"])
	restaurant_id=escape(request.POST["restaurant_id"])
	order_id=escape(request.POST["order_id"])
	time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	comment = escape(request.POST["comment"])
	rank =escape(request.POST["rank"])
	data = writeComment(user_id,dish_id,restaurant_id,order_id,time,comment,rank)
	return JsonResponse(data,safe=False)

def restaurant_like(request):
	restaurant_id=escape(request.POST["id"])
	like=escape(request.POST["like"])
	data = restaurantAddLike(restaurant_id,like)
	return JsonResponse(data,safe=False)

def insert_comment_photo(request):
	restaurant_id=escape(request.POST["restaurant_id"])
	dish_id=escape(request.POST["dish_id"])
	user_id=escape(request.POST["user_id"])
	photo_path=escape(request.POST["photo_path"])
	data=insertCommentPhoto(restaurant_id,dish_id,user_id,photo_path)
	return JsonResponse(data,safe=False)

def write_restaurant_sugestion(request):
	restaurant_id=escape(request.POST["restaurantID"])
	user_id=escape(request.POST["userID"])
	sugestion=escape(request.POST["sugestion"])
	data=writeRestaurantSugestion(restaurant_id,user_id,sugestion)
	return JsonResponse(data,safe=False)

def get_restaurant_sugestion(request):
	restaurant_id=escape(request.POST["restaurant_ID"])
	print("restaurant_id:"+restaurant_id)
	data=getRestaurantSugestion(restaurant_id)
	return JsonResponse(data,safe=False)

def restaurant_rank_list(request):
	print("restaurant_rank_list:")
	data=restaurantRankList()
	return JsonResponse(data,safe=False)

def dish_rank_list(request):
	restaurant_id=escape(request.POST["restaurant_id"])
	data=dishRankList(restaurant_id)
	return JsonResponse(data,safe=False)

def locate_file(request):
	request_file = request.get_full_path().replace('/canteen/static/', '')
	file_root = "C:/Users/Administrator/Desktop/lizhi/food_site/templates/static/"
	file_path = file_root + request_file
	file_path = urllib.parse.unquote(file_path)
	if file_path[len(file_path)-3:len(file_path)] == "png" or file_path[len(file_path)-3:len(file_path)] == "jpg" or file_path[len(file_path)-4:len(file_path)] == "jpeg" or file_path[len(file_path)-4:len(file_path)] == "JPEG":
		image_data = open(file_path,"rb").read()
		return HttpResponse(image_data,content_type="image/jpeg")
	elif file_path[len(file_path)-4:len(file_path)] == "webp":
		image_data = open(file_path,"rb").read()
		return HttpResponse(image_data,content_type="image/webp")
	elif file_path[len(file_path)-3:len(file_path)] == "css":
		css_data = open(file_path,"rb").read()
		return HttpResponse(css_data,content_type="text/css")
	else:
		return render(request, file_path)

def test(request):
	return render(request, "test.html")
