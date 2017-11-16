# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-12 01:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20171104_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'comprando'), (1, 'finalizada'), (2, 'fabricar'), (3, 'entregue')], default=0, verbose_name='Status'),
        ),
    ]