# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 02:16
from __future__ import unicode_literals

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('groupmanagement', '0006_request_groups_perm'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyGroup',
            fields=[
            ],
            options={
                'verbose_name': 'group',
                'indexes': [],
                'proxy': True,
                'verbose_name_plural': 'groups',
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='grouprequest',
            name='main_char',
        ),
    ]