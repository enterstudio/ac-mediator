# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 14:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20161025_1607'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servicecredentials',
            options={'verbose_name': 'service credentials', 'verbose_name_plural': 'service credentials'},
        ),
    ]
