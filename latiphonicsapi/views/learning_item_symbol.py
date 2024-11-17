from latiphonicsapi.models import Symbol, LearnItemSymbol, LearningSymbol, User
from rest_framework.viewsets import ViewSet
from rest_framework import status, serializers
from rest_framework.response import Response
from django.http import HttpResponseServerError

class LearningItemSymbolSerializer(serializers.ModelSerializer):
  class Meta:
    model = LearnItemSymbol
    fields = ('id','symbol', 'learning_symbol')
    depth = 1

class LearningItemSymbolView(ViewSet):
  def retrieve(self,request, pk):
    """gets individual LearningItemSymbol"""
    try:
      Learning_item = LearnItemSymbol.objects.get(pk=pk)
      serializer = LearningItemSymbolSerializer(Learning_item)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except LearnItemSymbol.DoesNotExist:
      return Response({'Boomer I could not find any Learning Item'})

  def list(self,request):
    """get all the Learning Items by user"""
    # Learning_items= LearnItemSymbol.objects.all()
    # for Learning_item in Learning_items:
    #     print(f'this is my learning items => {Learning_item.user.about}')
    # if not Learning_items.exists():
    #       return Response({'empty': '[]'}, status=status.HTTP_404_NOT_FOUND)
    # serializer =  LearningItemSymbolSerializer(Learning_items, many=True)
    # return Response(serializer.data, status=status.HTTP_200_OK)
    user_id = request.query_params.get('user_id')
    if not user_id:
      return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)
    Learning_items = LearnItemSymbol.objects.filter(user=user)

    if not Learning_items.exists():
        return Response({'empty': '[]'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LearningItemSymbolSerializer(Learning_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def create(self, request):
    """Create a new Learning Item"""
    symbol = Symbol.objects.get(pk=request.data['symbol'])
    learning_symbol = LearningSymbol.objects.get(pk=request.data['learning_symbol'])
    Learning_item = LearnItemSymbol.objects.create(
      symbol = symbol,
      learning_symbol = learning_symbol
    )
    serializer = LearningItemSymbolSerializer(Learning_item)
    return Response(serializer.data ,status=status.HTTP_201_CREATED)

  def destroy(self,request,pk):
    try:
        Learning_item=LearnItemSymbol.objects.get(pk=pk)
        Learning_item.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    except LearnItemSymbol.DoesNotExist:
      return Response({"Sorry I could not find your Learning Item"})
