from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("blank/", blank),
    path("index/", index),
    path("register/", register),
    path("get_code/", get_code),
    path("login/", login),
    path("logout/", logout),
    path("userprofile/", user_profile),
    path("goodsadd/", goods_add),
    path("add_label/", add_label),
    re_path(r"goodslist/(?P<page>\d+)/(?P<status>\d+)/", goods_list),
    re_path(r"goodsstatus/(?P<id>\d+)/(?P<status>\w+)/", goods_status),
    re_path(r"goodsrevise/(?P<id>\d+)/", goods_revise),
]
