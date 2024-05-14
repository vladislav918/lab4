from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.template.defaultfilters import slugify
from unidecode import unidecode


class Post(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    featured_image = models.ImageField(blank=True, default="default.jpg", upload_to="images/")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор", null=True)
    tag = models.ManyToManyField('Tag', blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название тега", unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    def __str__(self):
        return f"{self.name}"

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории", unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    def __str__(self):
        return f"{self.name}"


class Comment(models.Model):
    body = models.CharField(max_length=255, verbose_name="Комментарий")
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор")
    post = models.ForeignKey(Post, on_delete=models.PROTECT, verbose_name="Пост", related_name='comments')
