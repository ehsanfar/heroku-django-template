# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-01 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Join',
            fields=[
                ('bedroom', models.CharField(max_length=6, null=True)),
                ('bathroom', models.CharField(max_length=3, null=True)),
                ('neighborhood', models.CharField(default='nyc', max_length=100, null=True)),
                ('price', models.IntegerField(null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, max_length=120, null=True)),
                ('hashid', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('parent_neighborhood', models.CharField(max_length=20, null=True)),
                ('full_address', models.CharField(max_length=100, null=True)),
                ('listing_type_text', models.CharField(default='Apartment', max_length=10)),
                ('created_at', models.CharField(max_length=20, null=True)),
                ('linkurl', models.CharField(max_length=250, null=True)),
                ('source', models.IntegerField(null=True)),
                ('section', models.CharField(max_length=40, null=True)),
                ('excerpt', models.CharField(max_length=500, null=True)),
                ('isbroker', models.BooleanField(default=False)),
                ('isscam', models.BooleanField(default=False)),
                ('isemailsent', models.BooleanField(default=False)),
                ('hide', models.BooleanField(default=False)),
                ('emailtext', models.CharField(max_length=1000, null=True)),
                ('duplicategroupid', models.IntegerField(default=0, null=True)),
            ],
        ),
    ]