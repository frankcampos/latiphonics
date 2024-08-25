from rest_framework import status
from rest_framework.test import APITestCase
from datetime import date
from django.urls import reverse
from latiphonicsapi.models import LearnItemSymbol, Symbol, LearningSymbol, User
from latiphonicsapi.serializers import LearnItemSymbolSerializer

class TestLearningItemSymbol(APITestCase):
  def date_now(self):
    return date.today().strftime("%Y-%m-%dT00:00:00Z")

  def date_update(self):
      return date.today().strftime("%Y-%m-%dT00:00:00Z")

  def setUp(self):
    # create user instance
    self.user = User.objects.create(
            first_name='John',
            last_name='Doe',
            photo='photo_url',
            about='About John Doe',
            uid='unique_id_123'
        )

    # create a symbol instances
    self.symbol = Symbol.objects.create(
            picture_url="https://www.google.com",
            pronunciation="ah",
            is_voiced=True,
            is_vowel=True
            )
    #create a learning  symbol
    self.learning_symbol = LearningSymbol.objects.create(
      prompt = 'add an prompt',
      example_phrases = "phrases",
      video_url = 'google.com',
      user = self.user,
      created_at = self.date_now(),
      updated_at = self.date_update(),
    )

    #create a learning item symbol
    self.learning_item_symbol = LearnItemSymbol.objects.create(
      symbol = self.symbol,
      learning_symbol = self.learning_symbol
    )

    self.url = reverse('learn-item-symbol-detail', kwargs={'pk':self.learning_item_symbol.id})
    self.lists = reverse('learn-item-symbol-list')

    #  retrieve a learning item symbol
  def test_retrieve_learning_item_symbol(self):
    response = self.client.get(self.url)
    # I need another learning item symbol
    compare_response = LearnItemSymbol.objects.get(id=self.learning_item_symbol.id)
    # serializer my compare_response
    serializer = LearnItemSymbolSerializer(compare_response).data
    # compare the respond
    self.assertEqual(response.data, serializer)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # create a learning item symbol
  def test_create_learning_item_symbol(self):
    payload = {
      'symbol': self.symbol.id,
      'learning_symbol': self.learning_symbol.id

    }

    response = self.client.post(self.lists, payload)
    expected_respond = LearnItemSymbol.objects.last()
    serializer =  LearnItemSymbolSerializer(expected_respond).data
    self.assertEqual(response.data, serializer)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # list learning items symbol
  def test_get_all_learning_items_symbol(self):
    response = self.client.get(self.lists)
    expected_respond = LearnItemSymbolSerializer(LearnItemSymbol.objects.all(), many = True)
    self.assertEqual(response.data, expected_respond.data)

    #delete learning items symbol
    response = self.client.delete(self.url)
    self.assertEqual(response.data, {})
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
