# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joins', '0018_auto_20160801_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='join',
            name='available_date',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
