# Generated by Django 4.0.5 on 2022-06-13 14:35

import biblishelf_web.apps.plugins.book.models
import biblishelf_web.apps.main.fields
import biblishelf_web.apps.main.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biblishelf_book', '0005_alter_bookmodel_cover_alter_bookmodel_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='cover',
            field=biblishelf_web.apps.main.fields.PortableImageField(blank=True, default='', storage=biblishelf_web.apps.main.storage.PortableStorage, upload_to=biblishelf_web.apps.plugins.book.models._book_cover_uploader, verbose_name='cover'),
        ),
        migrations.AlterField(
            model_name='bookmodel',
            name='douban_id',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='bookmodel',
            name='isbn',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
    ]