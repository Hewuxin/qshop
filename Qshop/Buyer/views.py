# -*- coding: utf-8 -*-
# from Qshop.settings import alipay
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from Seller.models import *
from Buyer.models import *
import hashlib
from django.db.models import Sum
import random

# Create your views here.


def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def loginValid(func):
    def inner(request, *args, **kwargs):
        cookie_username = request.COOKIES.get("username")
        session_username = request.session.get("username")
        if cookie_username and session_username and cookie_username == session_username:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/login/")
    return inner


def base(request):
    return render(request, "buyer/base.html")

# UUID订单号


def get_order_no():
    import uuid
    order_no = str(uuid.uuid4())
    return order_no


@loginValid
def index(request):
    userid = request.COOKIES.get("userid")
    print(userid)
    # 实现首页商品展示只出现前4个
    goods_type = GoodsType.objects.all()
    res = []
    for one in goods_type:
        goods = one.goods_set.order_by('id').all()
        if len(goods) > 4:
            goods_list = goods[:4]
            res.append({"type": one, "goods_list": goods_list})
        elif len(goods) > 0 and len(goods) <= 4:
            goods_list = goods
            res.append({"type": one, "goods_list": goods_list})
    # 计算购物车商品数量
    num = Cart.objects.all().count()

    return render(request, "buyer/index.html", locals())


def register(request):
    # print(request.POST)
    message = "welcome"
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        repassword = request.POST.get('cpwd')
        email = request.POST.get('email')
        flag = LoginUser.objects.filter(username=username).exists()
        if flag:
            message = "用户已存在"
        else:
            if username and password and repassword and password == repassword:
                LoginUser.objects.create(
                    username=username,
                    password=setPassword(password),
                    email=email)
                return HttpResponseRedirect("/login/")
            else:
                message = "参数为空或密码有误"

    return render(request, "buyer/register.html", locals())


def login(request):
    # print(request.POST)
    message = "welcome"
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        if username and password:
            user = LoginUser.objects.filter(
                username=username,
                password=setPassword(password),
                user_type=1).first()
            if user:
                print(user.user_type,type(user.user_type))
                response = HttpResponseRedirect("/")
                response.set_cookie("username", user.username)
                response.set_cookie("userid", user.id)
                request.session["username"] = user.username
                return response
            else:
                message = "账号密码不正确"
        else:
            message = "参数为空"

    return render(request, "buyer/login.html", locals())


def logout(request):
    response = HttpResponseRedirect('/login/')
    response.delete_cookie("username")
    response.delete_cookie("userid")
    del request.session["username"]
    return response


@loginValid
def detail(request):
    if request.method == "GET":
        goodsid = request.GET.get("goodsid")
        goods = Goods.objects.get(id=goodsid)
        print(goods)
    return render(request, "buyer/detail.html", locals())


@loginValid
def list(request):
    if request.method == "GET":
        search_key = request.GET.get("search_key")
        typeid = request.GET.get("typeid")
        if typeid:
            goods_list = Goods.objects.filter(goods_type=typeid)
            print(goods_list)
        elif search_key:
            goods_list = Goods.objects.filter(
                goods_name__contains=search_key).all()
            print(goods_list)
        else:
            goods_list = Goods.objects.all()
            print(goods_list)
    return render(request, "buyer/list.html", locals())


@loginValid
def place_order(request):
    # 获取前端传来的数据
    user_id = request.COOKIES.get("userid")
    orderid = request.GET.get("orderid")
    orderid = int(orderid)
    print(orderid)
    payorder = PayOrder.objects.get(id=orderid)
    print(payorder)
    ordergoods = payorder.ordergoods_set.all()

    return render(request, "buyer/place_order.html", locals())


@loginValid
def add_order(request):
    user_id = request.COOKIES.get("userid")
    goods_id = request.GET.get("goods_id")  # 添加商品的id
    buy_number = int(request.GET.get("buy_number"))  # 前端传来的商品数量
    single = request.GET.get("single")  # 是否为单品添加
    goods = Goods.objects.get(id=goods_id)  # 添加的商品数据

    # 直接购买直接生成一个新的订单
    payorder = PayOrder()
    payorder.order_no = get_order_no()
    payorder.order_status = 1
    payorder.order_total = buy_number * goods.goods_price
    payorder.order_buyer_id = int(user_id)
    payorder.save()

    # 判断是否为单品添加
    if single == "1":
        # 添加商品进该订单
        order = PayOrder.objects.get(order_no=payorder.order_no)
        ordergoods = OrderGoods()
        ordergoods.order = order
        ordergoods.goods = goods
        ordergoods.goods_price = goods.goods_price
        ordergoods.shop = goods.goods_store
        ordergoods.buy_number = buy_number
        ordergoods.buy_count = buy_number * goods.goods_price
        ordergoods.save()
    else:
        pass

    # 生成新订单的id
    orderid = payorder.id
    print(orderid)
    result = {"orderid": orderid}

    return JsonResponse(result)


def cart_palce_order(request):
    data = request.POST
    res = []  # 购物车id
    for key, value in data.items():
        # print(key)
        # print(value)
        if key.startswith("cart_id"):
            res.append(value)
    print(res)
    # 将购物中选中的商品 生成订单
    user_id = request.COOKIES.get("userid")
    # 查找商品

    # 生成新的订单
    payorder = PayOrder()
    payorder.order_no = get_order_no()
    payorder.order_status = 1  # 未支付状态
    payorder.order_total = 0  # 订单总价  =  订单详情中的小计的和
    payorder.order_buyer_id = int(user_id)
    payorder.save()

    # ### 生成订单详情
    for one in res:
        # 查找购物车
        cart = Cart.objects.filter(id=one).first()
        ordergoods = OrderGoods()
        ordergoods.order = payorder
        ordergoods.goods = cart.goods
        ordergoods.goods_price = cart.goods.goods_price
        ordergoods.shop = cart.goods.goods_store
        ordergoods.buy_number = cart.goods_number
        ordergoods.buy_count = cart.goods_number * cart.goods.goods_price
        ordergoods.save()
        cart.delete()

    payorder_total = payorder.ordergoods_set.aggregate(
        sum_total=Sum("buy_count")).get("sum_total")
    payorder.order_total = payorder_total
    payorder.save()

    order_id = str(payorder.id)
    print(order_id)

    return render(request, "buyer/place_order.html", locals())
    # return HttpResponseRedirect(url)


@loginValid
def cart(request):
    user_id = request.COOKIES.get("userid")
    cart = Cart.objects.filter(
        cart_user=LoginUser.objects.get(
            id=int(user_id))).all()
    all_total = cart.aggregate(
        sum_total=Sum("goods_total"),
        sum_number=Sum("goods_number"))
    return render(request, "buyer/cart.html", locals())


@loginValid
def add_cart(request):
    result = {"code": 10000, "msg": "添加购物车成功"}
    data = request.POST
    # 从cookie中获取买家
    user_id = request.COOKIES.get("userid")
    print(data)
    goods_id = data.get("goods_id")
    goods_num = int(data.get("goods_num"))
    goods = Goods.objects.get(id=goods_id)
    allnum = goods.goods_number
    if goods_num == 0:
        result = {"code": 10001, "msg": "没有选择商品件数"}
    else:
        # 判断之前是否添加过
        cart = Cart.objects.filter(goods=goods_id).first()
        if cart:
            cart.goods_number += goods_num
            cart.goods_total += goods.goods_price * goods_num
        else:
            # 添加购物车
            cart = Cart()
            cart.goods = goods
            cart.goods_number = goods_num
            cart.goods_total = goods.goods_price * goods_num
            cart.cart_user_id = user_id
        try:
            if allnum >= cart.goods_number:
                cart.save()
                result = {"code": 10000, "msg": "添加购物车成功"}
            else:
                result = {"code": 10004, "msg": "库存不足"}
        except BaseException:
            result = {"code": 10001, "msg": "添加购物车失败"}

    return JsonResponse(result)


@loginValid
def change_cart(request):
    result = {"code": 10001, "msg": "计算失败", "data": {}}
    cart_id = request.POST.get("cart_id")
    js_type = request.POST.get("js_type")
    if cart_id and js_type:
        cart = Cart.objects.filter(id=int(cart_id)).first()
        allnum = cart.goods.goods_number
        if cart:
            if js_type == "add":
                cart.goods_number += 1
                cart.goods_total += cart.goods.goods_price
            else:
                cart.goods_number -= 1
                cart.goods_total -= cart.goods.goods_price
            try:
                if allnum >= cart.goods_number and cart.goods_number >= 0:
                    cart.save()
                    result = {
                        "code": 10000,
                        "msg": "修改操作成功",
                        "data": {
                            "goods_number": cart.goods_number,
                            "goods_total": cart.goods_total}}
                else:
                    result = {"code": 10004, "msg": "库存不够或商品不能再少了"}
            except BaseException:
                result = {"code": 10003, "msg": "操作失败"}
        else:
            result = {"code": 10002, "msg": "商品不存在"}
    return JsonResponse(result)


@loginValid
def delete_cart(request):
    result = {"code": 10000, "msg": "删除成功"}
    cart_id = request.POST.get("cart_id")
    print(cart_id)
    Cart.objects.filter(id=int(cart_id)).delete()
    return JsonResponse(result)


def user_center_info(request):
    return render(request, "buyer/user_center_info.html", locals())


def user_center_order(request):
    return render(request, "buyer/user_center_order.html", locals())


def user_center_site(request):
    return render(request, "buyer/user_center_site.html", locals())

#
# @loginValid
# def alipay_order(request):
#     payorder_id = request.GET.get("payorder_id")
#     payorder = PayOrder.objects.get(id=payorder_id)
#     order_string = alipay.api_alipay_trade_page_pay(
#         subject="电商交易",
#         out_trade_no=payorder.order_no,
#         total_amount=str(payorder.order_total + 10),
#         return_url="http://127.0.0.1:8000/buyer/pay_result/",
#         notify_url=None
#
#     )
#     result = "https://openapi.alipaydev.com/gateway.do?" + order_string
#     print(result)
#     return HttpResponseRedirect(result)

#
# @loginValid
# def pay_result(request):
#     out_trade_no = request.GET.get("out_trade_no")
#     payorder = PayOrder.objects.get(order_no=out_trade_no)
#     payorder.order_status = 2
#     payorder.save()
#     message = "支付成功！"
#     return render(request, "buyer/pay_result.html", locals())


# def add_order(request):
#     user_id = request.COOKIES.get("userid")
#     goods_id = request.GET.get("goods_id") #添加商品的id
#     buy_number = int(request.GET.get("buy_number")) #前端传来的商品数量
#     goods = Goods.objects.get(id=goods_id) #添加的商品数据
#     order_flag = PayOrder.objects.filter(order_buyer=user_id, order_status=1).exists()
#     #判断是否存在没有结账的订单
#     if order_flag == False:
#         payorder = PayOrder()
#         payorder.order_no = get_order_no()
#         payorder.order_status = 1
#         payorder.order_total = buy_number * goods.goods_price
#         payorder.order_buyer_id = int(user_id)
#         payorder.save()
#
#     #已有未结账订单，将商品存入订单
#
#     #查找未结账订单
#     order = PayOrder.objects.filter(order_buyer=user_id,order_status=1).first()
#     # 判断是否是商品之前是否添加过
#     havegoods = order.ordergoods_set.filter(goods_id = goods).exists()
#     if havegoods: #如果商品之前添加过
#         havegoodsnum = order.ordergoods_set.filter(goods_id=goods).values("buy_number")
#         print(havegoodsnum)
#         beforenum = havegoodsnum[0]["buy_number"]  # 获取原添加的数量
#         print(beforenum)
#         #获取该商品
#         havegoodsdata = OrderGoods.objects.get(goods=goods_id)
#         havegoodsdata.buy_number = beforenum + buy_number
#         print(havegoodsdata.buy_number)
#         havegoodsdata.buy_count = (beforenum + buy_number)* goods.goods_price
#         print(havegoodsdata.buy_count)
#         havegoodsdata.save()
#     else:
#         ordergoods = OrderGoods()
#         ordergoods.order = order
#         ordergoods.goods = goods
#         ordergoods.goods_price = goods.goods_price
#         ordergoods.shop = goods.goods_store
#         ordergoods.buy_number = buy_number
#         ordergoods.buy_count = buy_number * goods.goods_price
#         ordergoods.save()
#
#     #计算订单里的总价
#     order01 = PayOrder.objects.filter(order_buyer=user_id, order_status=1).first()
#     sumpric = order01.ordergoods_set.aggregate(buy_count=Sum("buy_count"))
#     sumprice = sumpric["buy_count"]
#     print(sumprice)
#     #保存到订单的total
#     newcount = PayOrder.objects.filter(order_buyer=user_id, order_status=1).first()
#     newcount.order_total = sumprice
#     newcount.save()
#     result = {"msg":"添加成功！"}
#     return JsonResponse(result)
