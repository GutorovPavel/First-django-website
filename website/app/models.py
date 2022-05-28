from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.
from django.urls import reverse


class User(AbstractUser):
    blocked = models.BooleanField(default=False)
    roles = (
        ('Bro', 'Bro'),
        ('Editor', 'Editor'),
    )
    role = models.CharField(max_length=30, choices=roles, default=roles[0][1])

    @property
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name


class Artist(models.Model):
    name = models.CharField(max_length=255)
    nick = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    image = models.ImageField(upload_to="photos/%Y/%m/%d")
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.nick

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

