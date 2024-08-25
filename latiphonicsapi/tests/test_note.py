from latiphonicsapi.models import Note, LearningSymbol, User
from latiphonicsapi.views import noteSerializer
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
from django.urls import reverse_lazy
from django.http import HttpResponseServerError

class NoteTest(APITestCase):
    def date_now(self):
        return date.today().strftime("%Y-%m-%dT00:00:00Z")

    def date_update(self):
        return date.today().strftime("%Y-%m-%dT00:00:00Z")

    def printLearningSymbol(self):
        ls = LearningSymbol.objects.first()
        print(ls)

    def setUp(self):
        # create user instance
        self.user = User.objects.create(
            first_name='John',
            last_name='Doe',
            photo='photo_url',
            about='About John Doe',
            uid='unique_id_123'
        )

        # create a learning symbol
        self.learning_symbol = LearningSymbol.objects.create(
            prompt='add an prompt',
            example_phrases='phrases',
            video_url='google.com',
            user=self.user,
            created_at=self.date_now(),
            updated_at=self.date_update(),
        )
        self.note = Note.objects.create(
            learning_item=self.learning_symbol,
            note_text='my first note text'
        )

        self.printLearningSymbol()

        self.detail_url = reverse_lazy('note-detail', kwargs={'pk': self.note.id})
        self.list_url = reverse_lazy('note-list')

    # get a note
    def test_get_note(self):
        response = self.client.get(self.detail_url)
        expected_response = noteSerializer(self.note).data
        self.assertEqual(response.data, expected_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_note_no_pk_found(self):
        url = reverse_lazy('note-detail', kwargs={'pk': 888})
        response = self.client.get(url)
        self.assertEqual(response.data, {'Boomer I could not find any note'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_notes(self):
        response = self.client.get(self.list_url)
        expected_response = noteSerializer(Note.objects.all(), many=True).data
        self.assertEqual(response.data, expected_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_notes_empty(self):
        Note.objects.all().delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.data, {'empty': '[]'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_note(self):
        data = {
            'learning_item': self.learning_symbol.id,
            'note_text': 'new note text'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['note_text'], 'new note text')

    def test_update_note(self):
        data = {
            'learning_item': self.learning_symbol.id,
            'note_text': 'updated note text'
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['note_text'], 'updated note text')

    def test_update_note_no_pk_found(self):
        url = reverse_lazy('note-detail', kwargs={'pk': 888})
        data = {
            'learning_item': self.learning_symbol.id,
            'note_text': 'updated note text'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.data, {"Sorry I could not find your note"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_note(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Note.objects.filter(pk=self.note.id).exists())

    def test_delete_note_no_pk_found(self):
        url = reverse_lazy('note-detail', kwargs={'pk': 888})
        response = self.client.delete(url)
        self.assertEqual(response.data, {"Sorry I could not find your note"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
