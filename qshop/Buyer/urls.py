from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("base/", base),
    path("index/", index),
    path("register/", register),
    path("login/", login),
    path("logout/", logout),

    path("list/", list),
    path("detail/", detail),
    path("add_order/", add_order),
    path("cart_palce_order/", cart_palce_order),

    path("cart/", cart),
    path("add_cart/", add_cart),
    path("change_cart/", change_cart),
    path("delete_cart/", delete_cart),

    path("placeorder/", place_order),
    path("usercenterinfo/", user_center_info),
    path("usercenterorder/", user_center_order),
    path("usercentersite/", user_center_site),
]
