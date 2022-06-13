# Generated by Django 4.0.5 on 2022-06-12 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biblishelf_book', '0003_alter_bookmodel_publisher_alter_bookmodel_set_book'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmodel',
            name='set_book',
        ),
        migrations.RemoveField(
            model_name='bookmodel',
            name='set_type',
        ),
        migrations.AddField(
            model_name='bookmodel',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='biblishelf_book.bookmodel'),
        ),
    ]