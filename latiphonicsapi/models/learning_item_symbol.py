from django.db import models
# what is not imported? 
#it was using a diferent python interpeter
from .symbol import Symbol
from .learning_symbol import LearningSymbol
from .user import User

# I need the user Id or UID
class LearnItemSymbol(models.Model):
  symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, null=True)
  learning_symbol = models.ForeignKey(LearningSymbol, on_delete=models.CASCADE, null=True)
  user= models.ForeignKey(User, on_delete=models.CASCADE, null=True)