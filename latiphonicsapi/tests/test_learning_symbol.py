from  latiphonicsapi.models import LearningSymbol, User
from latiphonicsapi.views import LearningSymbolSerializer
from rest_framework.test import APITestCase
from datetime import date
from django.urls import reverse
from django.http import HttpResponseServerError

class LearningSymbolTests(APITestCase):
  def date_now(self):
    return date.today().strftime("%Y-%m-%dT00:00:00Z")

  def date_update(self):
      return date.today().strftime("%Y-%m-%dT00:00:00Z")

  def setUp(self):
    self.user = User.objects.create(
            first_name='John',
            last_name='Doe',
            photo='photo_url',
            about='About John Doe',
            uid='unique_id_123'
        )

    self.LearningSymbol = LearningSymbol.objects.create(
      prompt = 'add an prompt',
      example_phrases = "phrases",
      video_url = 'google.com',
      user = self.user,
      created_at = self.date_now(),
      updated_at = self.date_update(),
    )
    self.url = reverse('learning-symbol-detail', kwargs={'pk':self.LearningSymbol.pk})

    self.lists = reverse('learning-symbol-list')

  def test_get_learning_symbol(self):
    response = self.client.get(self.url)
    respond_expected = LearningSymbolSerializer(self.LearningSymbol).data
    self.assertEqual(response.data, respond_expected)

# get all the learning Symbols
  def test_get_all_learning_symbols(self):
    response = self.client.get(self.lists)
    list_learning_symbols = LearningSymbol.objects.all()
    expected_respond = LearningSymbolSerializer(list_learning_symbols, many = True)
    self.assertEqual(response.data, expected_respond.data)

# create learning symbol
  def test_create_learning_symbol(self):
    data = {
      "prompt": 'new prompt',
      'example_phrases':'new phrases',
      'video_url': 'yahoo.com',
      'user': self.user.id,
      'created_at': self.date_now(),
      'updated_at': self.date_update()

      }
    respond = self.client.post(self.lists, data, format="json")
    expected_respond = LearningSymbol.objects.last()
    serializer_expected_respond = LearningSymbolSerializer(expected_respond)
    self.assertEqual(respond.data, serializer_expected_respond.data)



# update learning symbol
  def test_update_learning_symbol(self):
    data = {
        "prompt": 'updated prompt',
        'example_phrases':'updted phrases',
        'video_url': 'yahoo.com',
        'user': self.user.id,
        'created_at': self.date_now(),
        'updated_at': self.date_update()

        }
    respond = self.client.put(self.url, data, format="json")
    expected_respond = LearningSymbol.objects.last()
    serializer_expected_respond = LearningSymbolSerializer(expected_respond)
    self.assertEqual(respond.data, serializer_expected_respond.data)

# delete learning symbol
  def test_delete_symbol(self):
    response = self.client.delete(self.url)
    self.assertEqual(response.data , {})
