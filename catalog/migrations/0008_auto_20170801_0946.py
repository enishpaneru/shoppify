# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-01 04:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_rentinfo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dress',
            options={'ordering': ['-name']},
        ),
        migrations.AddField(
            model_name='dress',
            name='dress_pic2',
            field=models.FileField(blank=True, null=True, upload_to='images/dresspics/'),
        ),
    ]