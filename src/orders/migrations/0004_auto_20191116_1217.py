# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-11-16 12:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20191116_1213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='toatl',
            new_name='total',
        ),
    ]
