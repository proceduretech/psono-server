# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-25 15:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0009_auto_20171007_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='authkey',
            field=models.CharField(max_length=128, null=True, verbose_name='auth key'),
        ),
    ]