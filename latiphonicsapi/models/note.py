from django.db import models
from .learning_symbol import LearningSymbol

class Note(models.Model):
  learning_item = models.ForeignKey(LearningSymbol, on_delete=models.CASCADE, null=True)
  note_text = models.CharField(max_length=300000)
