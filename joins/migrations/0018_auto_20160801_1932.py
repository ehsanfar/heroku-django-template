# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 19:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joins', '0017_auto_20160801_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='join',
            name='parent_neighborhood',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
