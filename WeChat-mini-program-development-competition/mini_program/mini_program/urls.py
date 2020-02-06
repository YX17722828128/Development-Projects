"""mini_program URL Configuration

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
from account.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
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
    url(r'^aaa/$', mp4_file),
]