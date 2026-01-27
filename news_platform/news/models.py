from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Tovar(models.Model):
    title = models.TextField(max_length=255)
    text = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='img_news/', blank=True, verbose_name="Изображение")
    author = models.TextField(max_length=30)

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=25)
    subscribers = models.ManyToManyField(User, related_name='subscribers', blank=True)
    def __str__(self):
        return self.name