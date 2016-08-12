# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joins', '0004_auto_20160711_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='join',
            name='source',
            field=models.CharField(default='joinery', max_length=20),
        ),
        migrations.AlterField(
            model_name='neighborhood',
            name='area',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='neighborhood',
            name='parentarea',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='neighborhood',
            name='source',
            field=models.CharField(default='joinery', max_length=20),
        ),
    ]
