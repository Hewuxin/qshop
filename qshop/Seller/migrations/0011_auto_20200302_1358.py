# Generated by Django 2.2.1 on 2020-03-02 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0010_auto_20200227_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='goods_top',
            field=models.IntegerField(choices=[(1, '不推荐'), (0, '推荐')], default=1, verbose_name='产品推荐'),
        ),
    ]
