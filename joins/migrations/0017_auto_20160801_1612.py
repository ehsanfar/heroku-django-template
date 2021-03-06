# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joins', '0016_auto_20160728_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='join',
            name='images',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='join',
            name='messages',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='join',
            name='slug',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='join',
            name='views',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='neighborhood',
            name='shid',
            field=models.IntegerField(null=True),
        ),
    ]
