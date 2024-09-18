from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from latiphonicsapi.models import LearningSymbol, Note
from latiphonicsapi.serializers import LearningSymbolSerializer
from django.http import HttpResponseServerError

class noteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'learning_item', 'note_text')

class NoteView(ViewSet):
    def retrieve(self, request, pk):
        try:
            note = Note.objects.get(pk=pk)
            serializer = noteSerializer(note)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Note.DoesNotExist:
            return Response({'Boomer I could not find any note'}, status= status.HTTP_404_NOT_FOUND)

    def list(self, request):
        notes = Note.objects.all()
        if not notes.exists():
            return Response([], status=status.HTTP_404_NOT_FOUND)
        serializer = noteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        learning_item = LearningSymbol.objects.get(pk=request.data['learning_item'])
        note = Note.objects.create(
            learning_item = learning_item,
            note_text = request.data['note_text']
        )
        serializer = noteSerializer(note)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        try:
            learning_item = LearningSymbol.objects.get(pk=request.data['learning_item'])
            note = Note.objects.get(pk=pk)
            note.learning_item = learning_item
            note.note_text = request.data['note_text']
            note.save()

            serializer = noteSerializer(note)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Note.DoesNotExist:
            return Response({"Sorry I could not find your note"},status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
      try:
          note = Note.objects.get(pk=pk)
          note.delete()

          return Response({}, status=status.HTTP_204_NO_CONTENT)
      except Note.DoesNotExist:
          return Response({"Sorry I could not find your note"},status=status.HTTP_404_NOT_FOUND)
