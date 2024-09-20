from django.db import models

class Symbol(models.Model):
  picture_url = models.CharField(max_length=57730500)
  pronunciation = models.CharField(max_length=88855500, default='add a sound')
  is_voiced = models.BooleanField(default=True)
  is_vowel = models.BooleanField(default=True)
  sound_url = models.CharField(max_length=3000000, default='no sound added yet')
