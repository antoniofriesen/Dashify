from django.db import models

# Create your models here.

class Post(models.Model):
    title: str = models.CharField(max_length=75)
    body: str = models.TextField()
    slug: str = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)

    """ Methoden """
    def __str__(self) -> str:
        return self.title