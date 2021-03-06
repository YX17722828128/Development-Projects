"""foodsite-application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from library.views import *
from account.views import *
from food_site.views import *

urlpatterns = [
    url(r'^lib/admin/', admin.site.urls),
    url(r'^lib/return_book/$', return_book),
    url(r'^lib/storage_book/$', storage_book),
    url(r'^lib/ajax_storage_book/$', ajax_storage_book),
    url(r'^lib/home/$', home),
    url(r'^lib/library/$', redirect),
    url(r'^lib/book_detail/$', book_detail),
    url(r'^lib/template/$', template), 
    url(r'^wx/$', get),
    url(r'^lib/wx_redirect/$', wx_redirect),
    url(r'^lib/auto_share_config/$', auto_share_config),

    url(r'^$', demo_summary),

    url(r'^test/$', test),
    url(r'^login/$', login),
    url(r'^add_account_book/$', add_account_book),
    url(r'^delete_account_book/$', delete_account_book), 
    url(r'^add_type/$', add_type),
    url(r'^delete_type/$', delete_type),
    url(r'^add_balance_record/$', add_balance_record),
    url(r'^delete_balance_record/$', delete_balance_record),
    url(r'^show_balance/$', show_balance),
    url(r'^get_account_books/$', get_account_books),
    url(r'^get_account_types/$', get_account_types), 
    url(r'^handle_book/$', handle_book),
    url(r'^book_transfer/$', book_transfer),
    url(r'^exchange_rate/$', exchange_rate),
    url(r'^first_login/$', first_login),

    url(r'.well-known/pki-validation/fileauth.txt', TemplateView.as_view(template_name="fileauth.txt")),

    url(r'^video/$', mp4_file),

    url(r'^canteen/$', TemplateView.as_view(template_name="canteenIndex.html")),
    url(r'^canteen/static/', locate_file),
    url(r'^dish/$', dish),
    url(r'^order/$', order),
    url(r'^get_comments/$', get_comments),
    url(r'^search_dishes/$', search_dishes),
    url(r'^write_comments/$',write_comments),
    url(r'^restaurant_like/$',restaurant_like),
    url(r'^insert_comment_photo/$',insert_comment_photo),
    url(r'^write_restaurant_sugestion/$',write_restaurant_sugestion),
    url(r'^get_restaurant_sugestion/$',get_restaurant_sugestion),
    url(r'^restaurant_rank_list/$',restaurant_rank_list),
    url(r'^dish_rank_list/$',dish_rank_list),
]
