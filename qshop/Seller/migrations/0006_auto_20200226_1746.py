# Generated by Django 2.2.1 on 2020-02-26 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0005_auto_20200226_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='goods_store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Seller.LoginUser'),
        ),
        migrations.AddField(
            model_name='goods',
            name='goods_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Seller.GoodsType'),
        ),
        migrations.AlterField(
            model_name='loginuser',
            name='gender',
            field=models.IntegerField(choices=[(1, '男'), (0, '女')], default=1, verbose_name='性别'),
        ),
    ]
