from rest_framework import serializers
from .models import LearningSymbol, LearnItemSymbol

class LearningSymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningSymbol
        fields = ['id', 'prompt', 'example_phrases', 'video_url', 'user', 'created_at', 'updated_at']

class LearnItemSymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnItemSymbol
        fields = ['id', 'symbol', 'learning_symbol']
