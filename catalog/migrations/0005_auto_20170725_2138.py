# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-25 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_transaction_completion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='completion',
        ),
        migrations.AddField(
            model_name='dress',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
