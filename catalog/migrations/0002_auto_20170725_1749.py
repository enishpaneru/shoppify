# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-25 12:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dress',
            name='rentday',
            field=models.PositiveIntegerField(help_text='Days of rent you would allow'),
        ),
    ]