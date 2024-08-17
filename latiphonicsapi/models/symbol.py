from django.db import models

class Symbol(models.Model):
  picture_url = models.CharField(max_length=100)
  is_voiced = models.BooleanField(default=True)
  is_vowel = models.BooleanField(default=True)
