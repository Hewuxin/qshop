from django.db import models

# Create your models here.
GENDER_STATUS = {
    (0, "女"),
    (1, "男"),
}


class LoginUser(models.Model):
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱", null=True, blank=True)
    mobile_phone = models.CharField(
        max_length=11,
        verbose_name="手机号",
        null=True,
        blank=True)
    age = models.IntegerField(verbose_name="年龄", null=True, blank=True)
    gender = models.IntegerField(
        choices=GENDER_STATUS,
        verbose_name="性别",
        default=1)
    address = models.CharField(
        max_length=32,
        verbose_name="地址",
        null=True,
        blank=True)
    photo = models.ImageField(
        upload_to="img",
        default="img/cs01.jpg",
        verbose_name="图片")
    user_type = models.IntegerField(default=1, verbose_name="用户身份")  # 0卖家 1买家

    class Meta:
        db_table = "loginuser"
        verbose_name_plural = "用户信息"


class GoodsType(models.Model):
    type_label = models.CharField(max_length=32, verbose_name='类型标签')
    type_description = models.TextField(verbose_name='类型描述')
    type_picture = models.ImageField(max_length=64, verbose_name="类型图片")

    class Meta:
        db_table = "goods_type"
        verbose_name_plural = "产品类型"


GOODS_TOPS = {
    (0, "推荐"),
    (1, "不推荐"),
}


class Goods(models.Model):
    goods_no = models.CharField(max_length=32, verbose_name="商品编号")
    goods_name = models.CharField(max_length=32, verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品价格")
    goods_number = models.IntegerField(verbose_name="商品数量")
    goods_location = models.CharField(max_length=32, verbose_name="商品产地")
    goods_safe_time = models.IntegerField(verbose_name="产品保质期")
    goods_pro_time = models.DateTimeField(auto_now=True, verbose_name="添加日期")
    goods_status = models.IntegerField(
        verbose_name="商品状态", default=1)  # 0下架 1上架
    goods_picture = models.ImageField(
        upload_to="goodsimg",
        default="img/1.jpg",
        verbose_name="商品图片")
    goods_type = models.ForeignKey(
        to=GoodsType,
        on_delete=models.CASCADE,
        default=1)
    goods_store = models.ForeignKey(
        to=LoginUser, on_delete=models.CASCADE, default=1)
    goods_tip = models.TextField(
        max_length=32,
        verbose_name="商品简介",
        default="见详情页")
    goods_description = models.TextField(
        max_length=64, verbose_name="商品描述", default="good~")
    goods_top = models.IntegerField(
        choices=GOODS_TOPS,
        verbose_name="产品推荐",
        default=1)  # 0推荐 #1不推荐
    goods_click = models.IntegerField(verbose_name="点击量", default=0)

    class Meta:
        db_table = "goods"
        verbose_name_plural = "商品列表"


class ValidCode(models.Model):
    email = models.EmailField(max_length=32, verbose_name="用户邮箱")
    code = models.CharField(max_length=8, verbose_name="验证码")
    create_time = models.DateTimeField(auto_now=True, verbose_name="验证码创建时间")

    class Meta:
        db_table = "validcode"
        verbose_name_plural = "验证码"
