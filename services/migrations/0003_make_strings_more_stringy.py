# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 23:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20161016_0135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupcache',
            name='service',
            field=models.CharField(choices=[('discourse', 'discourse'), ('discord', 'discord')], max_length=254, unique=True),
        ),
    ]