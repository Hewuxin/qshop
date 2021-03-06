# Generated by Django 2.2.1 on 2020-02-25 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0003_auto_20200225_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginuser',
            name='user_type',
            field=models.IntegerField(default=1, verbose_name='用户身份'),
        ),
        migrations.AlterField(
            model_name='loginuser',
            name='gender',
            field=models.IntegerField(choices=[(0, '女'), (1, '男')], default=1, verbose_name='性别'),
        ),
    ]
