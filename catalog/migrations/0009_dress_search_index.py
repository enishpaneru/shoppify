# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-02 00:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20170801_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='dress',
            name='search_index',
            field=models.PositiveIntegerField(blank=True, default=2),
            preserve_default=False,
        ),
    ]
