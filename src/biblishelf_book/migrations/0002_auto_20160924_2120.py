# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-24 13:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biblishelf_book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='resource',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='biblishelf_main.Resource'),
        ),
    ]
