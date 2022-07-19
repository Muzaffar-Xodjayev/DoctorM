from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Problems(models.Model):
    title=models.CharField(max_length=255)
    img = models.ImageField(upload_to='problems')
    slug=models.SlugField(unique=True)
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True, null=True)
    updated_at=models.DateTimeField(auto_now=True, null=True )

    def __str__(self):
        return self.title



class Feedback(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    text = models.TextField()

    def __str__(self):
        return self.title


