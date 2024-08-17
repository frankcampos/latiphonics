from django.db import models
from .symbol import Symbol
from .learning_symbol import LearningSymbol

class LearnItemSymbol(models.Model):
  symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, null=True)
  learning_symbol = models.ForeignKey(LearningSymbol, on_delete=models.CASCADE, null=True)
