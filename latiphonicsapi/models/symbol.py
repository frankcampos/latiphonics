from django.db import models

class Symbol(models.Model):
  picture_url = models.CharField(max_length=10000000)
  pronunciation = models.CharField(max_length=10000000, default='add a sound')
  is_voiced = models.BooleanField(default=True)
  is_vowel = models.BooleanField(default=True)
  sound_url = models.CharField(max_length=10000000, default='no sound added yet')
