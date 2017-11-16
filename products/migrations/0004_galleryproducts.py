# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-13 15:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20171026_1436'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=350, verbose_name='Imagem')),
                ('product', models.ForeignKey(default='https://res.cloudinary.com/graphic/image/upload/v1510583427/product-default_tifjsl.jpg', on_delete=django.db.models.deletion.CASCADE, to='products.Product', verbose_name='Produto')),
            ],
        ),
    ]