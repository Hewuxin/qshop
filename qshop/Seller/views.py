from sdk.sendemailyzm import sendemail
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from .models import *
import hashlib
import random

# Create your views here.


def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def loginValid(func):
    def inner(request, *args, **kwargs):
        cookie_username = request.COOKIES.get("susername")
        session_username = request.session.get("susername")

        if cookie_username and session_username and cookie_username == session_username:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/seller/login/")
    return inner


def blank(request):
    return render(request, "seller/blank.html")


@loginValid
def index(request):
    username = request.COOKIES.get("susername")
    return render(request, "seller/index.html", locals())


def register(request):

    message = "welcome"
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        code = str(request.POST.get('yzm'))
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        flag = LoginUser.objects.filter(email=email).exists()
        rcode = ValidCode.objects.filter(email=email).last().code

        if flag:
            message = "邮箱已存在"
        else:
            if email and username and password and repassword and password == repassword and rcode == code:
                LoginUser.objects.create(
                    username=username,
                    email=email,
                    password=setPassword(password),
                    user_type=0)
                return HttpResponseRedirect("/seller/login/")
            else:
                message = "参数为空或密码有误"

    return render(request, "seller/register.html", locals())


def login(request):

    message = "welcome"
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = LoginUser.objects.filter(
                username=username,
                password=setPassword(password),
                user_type=0).first()
            if user:
                response = HttpResponseRedirect("/seller/index/")
                response.set_cookie("susername", user.username)
                response.set_cookie("suserid", user.id)
                request.session["susername"] = user.username
                return response
            else:
                message = "账号密码不正确"
        else:
            message = "参数为空"

    return render(request, "seller/login.html", locals())


def logout(request):
    response = HttpResponseRedirect('/seller/login/')

    response.delete_cookie("susername")
    response.delete_cookie("suserid")

    del request.session["susername"]
    return response


@loginValid
def goods_list(request, status, page=1):
    goods = Goods.objects.filter(goods_status=status).order_by("id")
    paginator_obj = Paginator(goods, 5)
    page_obj = paginator_obj.page(page)
    page_num = page_obj.number  # 当前页
    page_all = paginator_obj.num_pages
    if page_all > 5:
        if page_num < 3:
            start = 0
            end = 5
        elif page_num > page_all - 2:
            start = page_all - 5
            end = page_all
        else:
            start = page_num - 3
            end = page_num + 2
    else:
        start = 0
        end = page_all
    page_range = paginator_obj.page_range[start:end]

    return render(request, "seller/goods_list.html", locals())


@loginValid
def goods_status(request, id, status):

    goods = Goods.objects.get(id=id)

    if status == "up":
        goods.goods_status = 1
        goods.save()
    else:
        goods.goods_status = 0
        goods.save()
    url = request.META.get("HTTP_REFERER")

    return HttpResponseRedirect(url)


@loginValid
def user_profile(request):

    userid = request.COOKIES.get('suserid')
    user = LoginUser.objects.get(id=userid)

    if request.method == 'POST':
        data = request.POST
        user.email = data.get("email")
        user.mobile_phone = data.get("mobile_phone")
        user.username = data.get("username")
        user.age = data.get("age")
        user.gender = data.get("gender")
        user.address = data.get("address")
        if request.FILES.get("img"):
            user.photo = request.FILES.get("img")
        user.save()
    return render(request, "seller/user_profile.html", locals())


@loginValid
def goods_add(request):
    goods_type = GoodsType.objects.all()

    if request.method == "POST":
        user_id = request.COOKIES.get("suserid")

        data = request.POST
        goods = Goods()
        goods.goods_no = data.get("goods_no")
        goods.goods_name = data.get("goods_name")
        goods.goods_number = data.get("goods_number")
        goods.goods_location = data.get("goods_location")
        goods.goods_safe_time = data.get("goods_safe_time")
        goods.goods_price = data.get("goods_price")
        goods.goods_picture = request.FILES.get("goodsimg")
        goods.goods_type_id = int(data.get("goods_type"))
        goods.goods_store = LoginUser.objects.get(id=user_id)
        goods.save()
    return render(request, "seller/goods_add.html", locals())


@loginValid
def add_label(request):
    GoodsType.objects.create(
        type_label="新鲜蔬菜",
        type_description="新鲜蔬菜",
        type_picture="imgages/banner05.jpg")
    GoodsType.objects.create(
        type_label="新鲜水果",
        type_description="新鲜水果",
        type_picture="imgages/banner01.jpg")
    GoodsType.objects.create(
        type_label="海鲜水产",
        type_description="海鲜水产",
        type_picture="imgages/banner02.jpg")
    GoodsType.objects.create(
        type_label="猪牛羊肉",
        type_description="猪牛羊肉",
        type_picture="imgages/banner03.jpg")
    GoodsType.objects.create(
        type_label="禽类蛋品",
        type_description="禽类蛋品",
        type_picture="imgages/banner04.jpg")
    GoodsType.objects.create(
        type_label="速冻食品",
        type_description="速冻食品",
        type_picture="imgages/banner06.jpg")
    return HttpResponse("类型添加成功")


@loginValid
def goods_revise(request, id):
    goods = Goods.objects.get(id=id)
    type = GoodsType.objects.all()
    if request.method == "POST":
        data = request.POST
        goods.goods_no = data.get("goods_no")
        goods.goods_name = data.get("goods_name")
        goods.goods_number = data.get("goods_number")
        goods.goods_location = data.get("goods_location")
        goods.goods_safe_time = data.get("goods_safe_time")
        goods.goods_price = data.get("goods_price")
        goods.goods_tip = data.get("goods_tip")
        goods.goods_top = data.get("goods_top")
        goods.goods_click = data.get("goods_click")
        goods.goods_description = data.get("goods_description")
        goods.goods_picture = request.FILES.get("goodsimg")
        goods.goods_type_id = int(data.get("goods_type"))
        goods.save()

    return render(request, "seller/goods_revise.html", locals())


def get_code(request):
    email = request.GET.get("email")
    code = random.randint(1000, 9999)

    parmas = {
        "subject": "天天生鲜注册验证",
        "content": "天天生鲜注册【验证码：{}】".format(code),
        "recver": """{},""".format(email)
    }
    try:
        sendemail(parmas)
        ValidCode.objects.create(email=email, code=code)
        result = {"code": 10000, "msg": "验证码已发送"}
    except BaseException:
        result = {"code": 10001, "msg": "验证码发送失败"}

    return JsonResponse(result)
