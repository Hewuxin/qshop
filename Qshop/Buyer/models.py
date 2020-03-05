from django.db import models
from Seller.models import LoginUser, Goods

# Create your models here.

ORDER_STATUS = (
    (1, "未支付"),
    (2, "已支付"),
    (3, "待发货"),
    (4, "已发货"),
    (5, "拒收"),
    (6, "已完成"),
)


class PayOrder(models.Model):
    order_no = models.CharField(max_length=64, unique=True, verbose_name="订单号")
    order_date = models.DateField(auto_now=True, verbose_name="订单创建时间")
    order_status = models.IntegerField(
        choices=ORDER_STATUS, verbose_name="订单状态")
    order_total = models.FloatField(verbose_name="订单总价")
    order_buyer = models.ForeignKey(
        to=LoginUser,
        on_delete=models.CASCADE,
        verbose_name="买家")

    class Meta:
        db_table = "pay_order"
        verbose_name_plural = "支付订单"


class OrderGoods(models.Model):
    order = models.ForeignKey(to=PayOrder, on_delete=models.CASCADE)
    goods = models.ForeignKey(to=Goods, on_delete=models.CASCADE)
    goods_price = models.FloatField(verbose_name="商品单价")
    shop = models.ForeignKey(
        to=LoginUser,
        on_delete=models.CASCADE,
        verbose_name="卖家")
    buy_number = models.IntegerField(verbose_name="购买单品数量")
    buy_count = models.FloatField(verbose_name="购买单品总价")

    class Meta:
        db_table = "order_goods"
        verbose_name_plural = "订单商品详情"


class Cart(models.Model):
    goods = models.ForeignKey(to=Goods, on_delete=models.CASCADE)
    goods_number = models.IntegerField(verbose_name="商品的数量")
    goods_total = models.FloatField(verbose_name="商品的小计")
    # goods_price = models.FloatField()
    cart_user = models.ForeignKey(
        to=LoginUser,
        on_delete=models.CASCADE,
        verbose_name="买家")

    class Meta:
        db_table = "cart"
