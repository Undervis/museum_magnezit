from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Item(models.Model):
    name = models.CharField("Название", max_length=64)
    description = models.TextField("Описание")
    time_create = models.DateTimeField("Дата добавления", auto_now_add=True)
    time_update = models.DateTimeField("Дата обновления", auto_now=True)
    date_story = models.CharField("Датировка", max_length=64)
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    image = models.ImageField("Фото", upload_to="static/images")
    index = models.CharField("Шифр", max_length=32)
    comment = models.TextField("Примечание", blank=True)
    fonds = models.ManyToManyField('Fond')
    isArchived = models.BooleanField("Экспонат списан", default=False)
    last_editor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                    verbose_name='Последний редактор')

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.name


class File(models.Model):
    fileDoc = models.FileField("Файл", upload_to='static/files', blank=True)
    itemId = models.IntegerField(blank=True)

    def __str__(self):
        return self.fileDoc.name

    class Meta:
        verbose_name = 'файл'
        verbose_name_plural = "Файлы"

    def get_file_name(self):
        return self.fileDoc.name[13:]


class Photo(models.Model):
    filePhoto = models.FileField("Фото", upload_to='static/images', blank=True)
    itemId = models.IntegerField(blank=True)

    def __str__(self):
        return self.filePhoto.name

    class Meta:
        verbose_name = 'фото'
        verbose_name_plural = "Фотографии"


class Category(MPTTModel):
    title = models.CharField("Категория", max_length=64)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    slug = models.SlugField()

    def __str__(self):
        return self.title

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return self.id


class Fond(models.Model):
    name = models.CharField("Название фонда", max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'фонд'
        verbose_name_plural = 'Фонды'