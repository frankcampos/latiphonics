from django.db import models
from django.utils import timezone

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.CharField(max_length=10000)
    about = models.CharField(max_length=50000)
    uid = models.CharField(max_length=1500)
