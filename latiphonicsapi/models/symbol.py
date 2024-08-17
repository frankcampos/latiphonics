from django.db import models
from django.utils import timezone

class Symbol(models.Model):
  picture_url = models.CharField(max_length=100)
  is_voiced = models.BooleanField
  is_vowel = models.BooleanField(default=True)
