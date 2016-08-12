# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 17:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joins', '0003_auto_20160706_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=20)),
                ('area', models.CharField(max_length=20)),
                ('nid', models.CharField(max_length=20)),
                ('parentarea', models.CharField(max_length=20)),
            ],
        ),
        migrations.RenameField(
            model_name='join',
            old_name='ftsquared',
            new_name='ft2',
        ),
    ]