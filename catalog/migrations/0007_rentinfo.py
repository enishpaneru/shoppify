# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-26 05:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20170726_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='rentinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fine', models.PositiveIntegerField()),
                ('insuranceclaimstatus', models.BooleanField(default=False)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.transaction')),
            ],
        ),
    ]