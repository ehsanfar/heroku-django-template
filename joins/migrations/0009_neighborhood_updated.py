# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-21 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joins', '0008_auto_20160720_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='neighborhood',
            name='updated',
            field=models.BooleanField(default=False),
        ),
    ]
