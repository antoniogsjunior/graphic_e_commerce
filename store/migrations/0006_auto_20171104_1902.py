# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-04 22:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20171104_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='value',
            field=models.FloatField(verbose_name='Valor'),
        ),
        migrations.AlterField(
            model_name='order',
            name='dateStart',
            field=models.DateTimeField(auto_now=True, verbose_name='Data Compra'),
        ),
        migrations.AlterField(
            model_name='order',
            name='valueTotal',
            field=models.FloatField(null=True, verbose_name='Valor Total'),
        ),
    ]