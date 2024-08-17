from django.db import models
from django.utils import timezone
from .user import User

class LearningSymbol(models.Model):
  prompt = models.TextField(max_length=200)
  example_phrases = models.TextField(max_length=200)
  video_url = models.CharField(max_length=100)
  user= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True, null=True)
