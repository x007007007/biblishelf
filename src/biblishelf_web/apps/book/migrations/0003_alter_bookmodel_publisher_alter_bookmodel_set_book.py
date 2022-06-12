# Generated by Django 4.0.5 on 2022-06-12 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biblishelf_book', '0002_rename_book_bookmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biblishelf_book.bookpublishing'),
        ),
        migrations.AlterField(
            model_name='bookmodel',
            name='set_book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_books', to='biblishelf_book.bookmodel'),
        ),
    ]
