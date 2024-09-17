from openai import OpenAI
import os
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from latiphonicsapi.models import User, Symbol, LearningSymbol, LearnItemSymbol
from latiphonicsapi.serializers import LearningSymbolSerializer, LearnItemSymbolSerializer

class AddSymbolToListView(ViewSet):

    @action(detail=False, methods=['post'])
    def add_to_list(self, request):
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        try:
            user_id = request.data['user_id']
            symbol_id = request.data['symbol_id']

            user = User.objects.get(pk=user_id)
            symbol = Symbol.objects.get(pk=symbol_id)

            # Generate prompt
            prompt = self.generate_prompt(user.about, symbol.pronunciation)

            # Make request to OpenAI API
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract generated phrases
            message_content = response.choices[0].message.content

            # Create LearningSymbol instance
            learning_symbol = LearningSymbol.objects.create(
                prompt=prompt,
                example_phrases=message_content,
                video_url=request.data.get('video_url', ''),
                user=user
            )

            # Create LearnItemSymbol instance
            learn_item_symbol = LearnItemSymbol.objects.create(
                symbol=symbol,
                learning_symbol=learning_symbol
            )

            return Response({
                'learning_symbol': LearningSymbolSerializer(learning_symbol).data,
                'learn_item_symbol': LearnItemSymbolSerializer(learn_item_symbol).data
            }, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Symbol.DoesNotExist:
            return Response({"detail": "Symbol not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def generate_prompt(self, about, pronunciation):
    #   return (
    #     f"Please create three example phrases using the pronunciation '{pronunciation}' "
    #     f"and provide their transcriptions in the International Phonetic Alphabet (IPA). "
    #     f"Each phrase should be relevant to the following user description: {about}. "
    #     "The output should strictly be in the following JSON format without any additional text:\n\n"
    #     "[\n"
    #     "  {\"phrase\": \"[Phrase 1]\", \"ipa\": \"[IPA transcription 1]\"},\n"
    #     "  {\"phrase\": \"[Phrase 2]\", \"ipa\": \"[IPA transcription 2]\"},\n"
    #     "  {\"phrase\": \"[Phrase 3]\", \"ipa\": \"[IPA transcription 3]\"}\n"
    #     "]"
    # )

    def generate_prompt(self, about, pronunciation):
        return (
            f"Please create three example phrases that emphasize the use of the phonetic sound '{pronunciation}'. "
            f"Each phrase should be related to the following user description: {about}, "
            f"and introduce new vocabulary to help the user expand their knowledge. "
            "Additionally, provide the phonetic transcription of each phrase in the International Phonetic Alphabet (IPA). "
            "The output should strictly be in the following JSON format without any additional text:\n\n"
            "[\n"
            "  {\"phrase\": \"[Phrase 1]\", \"ipa\": \"[IPA transcription 1]\"},\n"
            "  {\"phrase\": \"[Phrase 2]\", \"ipa\": \"[IPA transcription 2]\"},\n"
            "  {\"phrase\": \"[Phrase 3]\", \"ipa\": \"[IPA transcription 3]\"}\n"
            "]"
        )
