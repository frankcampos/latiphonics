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
  def retrieve(self,request, pk):
    """gets individual LearningSymbol"""
    try:
      Learning_symbol = LearningSymbol.objects.get(pk=pk)
      serializer = LearningSymbolSerializer(Learning_symbol)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except LearningSymbol.DoesNotExist:
      return Response({'Boomer I could not find any Learning Symbol'})
  def list(self,request):
    """get all the Learning Symbols"""
    Learning_symbols= LearningSymbol.objects.all()
    if not Learning_symbols.exists():
          return Response({'empty': '[]'}, status=status.HTTP_404_NOT_FOUND)
    serializer =  LearningSymbolSerializer(Learning_symbols, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def create(self, request):
    """Create a new Learning Symbol"""
    user = User.objects.get(pk=request.data['user'])
    Learning_symbol = LearningSymbol.objects.create(
      prompt = request.data['prompt'],
      example_phrases = request.data['example_phrases'],
      video_url = request.data['video_url'],
      user = user
    )
    serializer = LearningSymbolSerializer(Learning_symbol)
    return Response(serializer.data ,status=status.HTTP_201_CREATED)

  def update(self,request,pk):
    try:
        user = User.objects.get(pk=request.data['user'])
        Learning_symbol=LearningSymbol.objects.get(pk=pk)
        Learning_symbol.prompt = request.data['prompt']
        Learning_symbol.example_phrases = request.data['example_phrases']
        Learning_symbol.video_url = request.data['video_url']
        Learning_symbol.user = user
        Learning_symbol.save()

        serializer = LearningSymbolSerializer(Learning_symbol)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    except LearningSymbol.DoesNotExist:
      return Response({"Sorry I could not find your Learning Symbol"})

  def destroy(self,request,pk):
    try:
        Learning_symbol=LearningSymbol.objects.get(pk=pk)
        Learning_symbol.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    except LearningSymbol.DoesNotExist:
      return Response({"Sorry I could not find your Learning Symbol"})
