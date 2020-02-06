"""pxty URL Configuration

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
from manage.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^login_first/$', login_first),
    url(r'^sign_in/$', sign_in),
    url(r'^sign_up/$', sign_up),
    url(r'^carousel/$', carousel),
    url(r'^news/$', news),
    url(r'^upload_news/$', upload_news),
    url(r'^expense_application/$', expense_application),
    url(r'^news_list/$', news_list),
    url(r'^manage_carousel/$', manage_carousel),
    url(r'^establish_form/$', establish_form),
    url(r'^show_expense/$', show_expense),
    url(r'^check_expense/$', check_expense),
    url(r'^recommend_news/$', recommend_news),
    url(r'^part1_news_display/$', part1_news_display),
    url(r'^part2_news_display/$', part2_news_display),
    url(r'^part3_news_display/$', part3_news_display),
    url(r'^part4_news_display/$', part4_news_display),
    url(r'^news_page_content/$', news_page_content),
    url(r'^start_login/', start_login),
    url(r'^confirm_login/', confirm_login),
    url(r'^test/download_form/$', download_form),
    url(r'^test_file/$', test_file),
    url(r'^wx/$', get),
    url(r'^resource/', locate_file),
    url(r'^test/$', TemplateView.as_view(template_name="test.html")),
    url(r'MP_verify_ELQMap6wwKZ7EtWi.txt', TemplateView.as_view(template_name="MP_verify_ELQMap6wwKZ7EtWi.txt")),
]