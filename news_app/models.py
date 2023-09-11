from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
import requests
from django.utils.text import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    brief = models.TextField()
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images/')
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    trending = models.BooleanField(default=False)
    recent_news = models.BooleanField(default=True)
    # trending_video = models.BooleanField(default=False)
    popular_news = models.BooleanField(default=False)
    recent_reviews = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Generate a slug from the title before saving the instance
        self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-timestamp']  # Sort in descending order by timestamp
        
    def get_absolute_url(self):
        return reverse('news-detail', args=[str(self.slug)])

    