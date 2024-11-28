from typing import Iterable
from django.db import models
from django_jalali.db import models as jmodels
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class User(models.Model):
    role = models.CharField(max_length = 50)
class News(models.Model):
    title = models.CharField(max_length = 20 , null = True)
    text = models.CharField(max_length = 10000 , null = True)
    short_description=models.CharField(max_length = 15000 , null = True)
    date = jmodels.jDateTimeField(auto_now_add = True)
    user = models.ForeignKey(User , on_delete = models.CASCADE, null = True)
    slug = models.SlugField(default="" , null = False)

    def get_absolute_url(self):
        return reverse("model_detail", args={self.pk})
    
    def save(self , *args , **kwargs):
        self.slug = slugify(self.title)
        super().save(*args , **kwargs)
    
