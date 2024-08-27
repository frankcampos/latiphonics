from rest_framework import status
from rest_framework.test import APITestCase
from latiphonicsapi.models import User

class UserTests(APITestCase):
  def setUp(self):
      self.user = User.objects.create(first_name="Daniel",
          last_name="Campos",
          photo="https://www.google.com",
          about="I am a developer",
          uid="123456",
      )
  def test_register_user(self):
    url  = "/register"
    user = {
      "first_name": "Daniel",
      "last_name": "Campos",
      "photo": "https://www.google.com",
      "about": "I am a developer",
      "uid": "123456",
    }
    response = self.client.post(url, user, format='json')

    new_user = User.objects.last()
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_chek_user_invalid(self):
    url = "/checkuser"
    response = self.client.post(url, {'uid': '123456'}, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['first_name'], self.user.first_name)
    self.assertEqual(response.data['last_name'], self.user.last_name)
    self.assertEqual(response.data['photo'], self.user.photo)
    self.assertEqual(response.data['about'], self.user.about)
    self.assertEqual(response.data['uid'], self.user.uid)

  def test_delete_user(self):
    url = "/delete_user"
    response = self.client.delete(url, {'user_id': self.user.id}, format='json')
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

  def test_update_user(self):
    url = "/update_user"
    response = self.client.put(url, {
      'id': self.user.id,
      'first_name': 'Daniel',
      'last_name': 'Campos',
      'photo': 'https://www.google.com',
      'about': 'I am a developer',
    }, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['first_name'], 'Daniel')
    self.assertEqual(response.data['last_name'], 'Campos')
    self.assertEqual(response.data['photo'], 'https://www.google.com')
    self.assertEqual(response.data['about'], 'I am a developer')

  def test_get_user(self):
    url = "/get_user"
    user = User.objects.first()
    response = self.client.get(url, {'user_id': user.id}, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['first_name'], self.user.first_name)
    self.assertEqual(response.data['last_name'], self.user.last_name)
    self.assertEqual(response.data['photo'], self.user.photo)
    self.assertEqual(response.data['about'], self.user.about)
    self.assertEqual(response.data['uid'], self.user.uid)
