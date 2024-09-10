from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title: str = models.CharField(max_length=75)
    body: str = models.TextField()
    slug: str = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default="fallback.png", blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    """ Methoden """
    def __str__(self) -> str:
        return self.title