# Generated by Django 2.2.1 on 2020-02-26 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0007_auto_20200226_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='goods_top',
            field=models.IntegerField(choices=[(0, '推荐'), (1, '不推荐')], default=1, verbose_name='产品推荐'),
        ),
    ]