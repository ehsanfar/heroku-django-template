# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-26 17:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('joins', '0012_auto_20160726_1548'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userhist',
            old_name='alerthashid',
            new_name='alerthist',
        ),
    ]
