from latiphonicsapi.models import User,LearningSymbol
from rest_framework.viewsets import ViewSet
from rest_framework import status,serializers
from rest_framework.response import Response
from django.http import HttpResponseServerError

#create serializer for learning symbol
class LearningSymbolSerializer(serializers.ModelSerializer):
  class Meta:
    model = LearningSymbol
    fields = ('id','prompt', 'example_phrases','video_url','user','created_at','updated_at')

class LearningSymbolView(ViewSet):
  """_summary_

  Args:
      ViewSet (_type_): _description_
  """
  # def create(self, request):
  #   id = user.data['user_id']
  #   user = User.objects.get(id)

  #   user_about = user.about

  #   prompt = f'created the 3 phrases by using the IPA, international Phonetic alphabet'

  #   # should I create the relation ship with learning item symbol
