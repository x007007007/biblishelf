# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-20 16:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biblishelf_main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.PositiveIntegerField(default=0)),
                ('sha', models.CharField(blank=True, max_length=150, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('mine_type', models.CharField(blank=True, max_length=32, null=True)),
                ('ed2k_hash', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.RemoveField(
            model_name='resourcemap',
            name='sha',
        ),
        migrations.RemoveField(
            model_name='resourcemap',
            name='size',
        ),
        migrations.AddField(
            model_name='driver',
            name='extend_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='driver',
            name='online_status',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='driver',
            name='type',
            field=models.CharField(blank=True, choices=[('Disk', 'disk'), ('iso/img', 'img'), ('lfs', 'lfs')], max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='resourcemap',
            name='create_time',
            field=models.DateTimeField(blank=True, help_text='help check out danger file', null=True),
        ),
        migrations.AddField(
            model_name='resourcemap',
            name='modify_time',
            field=models.DateTimeField(blank=True, help_text='help check out danger file', null=True),
        ),
        migrations.AlterField(
            model_name='configwatcharea',
            name='path',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='driver',
            name='uuid',
            field=models.CharField(max_length=128, verbose_name='Volumn'),
        ),
        migrations.AlterField(
            model_name='resourcemap',
            name='path',
            field=models.CharField(max_length=1024),
        ),
        migrations.AddField(
            model_name='resourcemap',
            name='resource',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Map', to='biblishelf_main.Resource'),
        ),
    ]
