# Generated by Django 4.2.1 on 2023-05-26 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Категория')),
                ('slug', models.SlugField()),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='main.category', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'категорию',
                'verbose_name_plural': 'Категории',
                'unique_together': {('parent', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileDoc', models.FileField(blank=True, upload_to='static/files', verbose_name='Файл')),
                ('itemId', models.IntegerField(blank=True)),
            ],
            options={
                'verbose_name': 'файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
        migrations.CreateModel(
            name='Fond',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название фонда')),
            ],
            options={
                'verbose_name': 'фонд',
                'verbose_name_plural': 'Фонды',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filePhoto', models.FileField(blank=True, upload_to='static/images', verbose_name='Фото')),
                ('itemId', models.IntegerField(blank=True)),
            ],
            options={
                'verbose_name': 'фото',
                'verbose_name_plural': 'Фотографии',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('date_story', models.CharField(max_length=64, verbose_name='Датировка')),
                ('image', models.ImageField(upload_to='static/images', verbose_name='Фото')),
                ('index', models.CharField(max_length=32, verbose_name='Шифр')),
                ('comment', models.TextField(blank=True, verbose_name='Примечание')),
                ('isArchived', models.BooleanField(default=False, verbose_name='Экспонат списан')),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='main.category', verbose_name='Категория')),
                ('fonds', models.ManyToManyField(to='main.fond')),
                ('last_editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Последний редактор')),
            ],
            options={
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
            },
        ),
    ]