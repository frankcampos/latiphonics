from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from latiphonicsapi.models import Symbol
from latiphonicsapi.views import SymbolSerializer


class SymbolTests(APITestCase):
    def setUp(self):
        self.symbol = Symbol.objects.create(
            picture_url="https://www.google.com",
            pronunciation="ah",
            is_voiced=True,
            is_vowel=True
        )
        self.url = reverse('symbol-detail',
                           kwargs={'pk': self.symbol.pk})
    def test_get_symbol(self):
        response = self.client.get(f"/symbol/{self.symbol.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pronunciation"], "ah")
        self.assertEqual(response.data["is_voiced"], True)
        self.assertEqual(response.data["is_vowel"], True)
        self.assertEqual(response.data["picture_url"], "https://www.google.com")

    def test_create_symbol(self):
        url = "/symbol"
        data = {
            "picture_url": "https://www.google.com",
            "pronunciation": "ah",
            "is_voiced": True,
            "is_vowel": True
        }
        response = self.client.post(url, data, format="json")
        new_symbol = Symbol.objects.last()
        serializer = SymbolSerializer(new_symbol).data
        self.assertEqual(response.data, serializer)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  # test update symbol
    def test_update_symbol(self):
      url = f"/symbol/{self.symbol.id}"
      data = {
        "picture_url": "https://www.google.com",
        "pronunciation": "new pronunciation",
        "is_voiced": True,
        "is_vowel": True
      }
      response = self.client.put(url, data, format="json")
      self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
      self.assertEqual(response.data["pronunciation"], "new pronunciation")
      self.assertEqual(response.data["is_voiced"], True)
      self.assertEqual(response.data["is_vowel"], True)
      self.assertEqual(response.data["picture_url"], "https://www.google.com")

    # test delete symbol
    def test_delete_symbol(self):
      symbol_id = Symbol.objects.first()
      url ='/symbol/symbol_id.id'
      respond = self.client.delete(url)

  # test get all symbols
    def test_get_all_symbols(self):
      url = '/symbol'
      respond = self.client.get(url, format="json")
      symbols = Symbol.objects.all()
      serializer = SymbolSerializer(symbols, many=True)
      self.assertEqual(respond.data, serializer.data)
      self.assertEqual(respond.status_code, status.HTTP_200_OK )
  # test individual symbol
    def test_retrieve(self):
        respond = self.client.get(self.url)
        expected_data = SymbolSerializer(self.symbol).data
        self.assertEqual(respond.data, expected_data)
        self.assertEqual(respond.status_code, status.HTTP_200_OK)
