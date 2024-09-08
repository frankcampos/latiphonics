from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status,serializers
from latiphonicsapi.models import Symbol, LearnItemSymbol
from django.http import HttpResponseServerError

# class TreeSerializer(serializers.ModelSerializer):
#     compounds = serializers.SerializerMethodField()
#     def get_compounds(self, object):
#         return Compound.objects.filter(trees__tree_id=object)
#     class Meta:
#         model = Tree
#         fields = ('id', 'name', 'uid', 'compounds')


class SymbolSerializer(serializers.ModelSerializer):
    added = serializers.SerializerMethodField()
    def get_added(self,obj):
      return LearnItemSymbol.objects.filter(symbol=obj).exists()
    class Meta:
        model = Symbol
        fields = ('id', 'picture_url', 'is_voiced', 'is_vowel','pronunciation', 'added')

class SymbolView(ViewSet):

# retrieve method
  def retrieve(self,request, pk):
    """gets individual symbol """
    try:
      symbol = Symbol.objects.get(pk=pk)
      serializer = SymbolSerializer(symbol)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Symbol.DoesNotExist:
      return Response({'Boomer I could not find any symbol'})
    except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#list symbols
  def list(self,request):
    """get all the symbols"""
    symbols= Symbol.objects.all()
    if not symbols.exists():
          return Response({'empty': '[]'}, status=status.HTTP_404_NOT_FOUND)
    serializer =  SymbolSerializer(symbols, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# create symbols
  def create(self, request):
    """Create a new symbol(sound)"""
    symbol = Symbol.objects.create(
      picture_url = request.data['picture_url'],
      is_voiced = request.data['is_voiced'],
      is_vowel = request.data['is_vowel'],
      pronunciation = request.data['pronunciation']
    )
    serializer = SymbolSerializer(symbol)
    return Response(serializer.data ,status=status.HTTP_201_CREATED)

# update symbols
  def update(self,request,pk):
    try:
        symbol=Symbol.objects.get(pk=pk)
        symbol.picture_url = request.data['picture_url']
        symbol.is_voiced = request.data['is_voiced']
        symbol.is_vowel = request.data['is_vowel']
        symbol.pronunciation= request.data['pronunciation']
        symbol.save()

        serializer = SymbolSerializer(symbol)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    except Symbol.DoesNotExist:
      return Response({"Sorry I could not find your symbol"})
# delete symbols
  def destroy(self,request, pk):
    try:
      symbol = Symbol.objects.get(pk=pk)
      symbol.delete()
      serializer = SymbolSerializer(symbol)
      return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    except Symbol.DoesNotExist:
      return Response({'I could not find the symbol'}, status=status.HTTP_404_NOT_FOUND)
