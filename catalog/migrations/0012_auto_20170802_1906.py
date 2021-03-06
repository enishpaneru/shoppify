# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-02 13:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20170802_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dress',
            name='detail',
            field=models.TextField(help_text='Enter a brief description of the dress', max_length=1000),
        ),
        migrations.AlterField(
            model_name='dress',
            name='dress_pic2',
            field=models.FileField(blank=True, default=None, null=True, upload_to='images/dresspics/'),
        ),
    ]
