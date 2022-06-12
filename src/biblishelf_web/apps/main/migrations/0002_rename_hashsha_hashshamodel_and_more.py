# Generated by Django 4.0.5 on 2022-06-10 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biblishelf_book', '0001_initial'),
        ('biblishelf_main', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HashSha',
            new_name='HashShaModel',
        ),
        migrations.RenameModel(
            old_name='MineType',
            new_name='MineTypeModel',
        ),
        migrations.RenameModel(
            old_name='Path',
            new_name='PathModel',
        ),
        migrations.RenameModel(
            old_name='Repo',
            new_name='RepoModel',
        ),
        migrations.RenameModel(
            old_name='Resource',
            new_name='ResourceModel',
        ),
        migrations.CreateModel(
            name='SubRepoModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblishelf_main.repomodel')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblishelf_main.resourcemodel')),
            ],
        ),
    ]