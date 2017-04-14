"""Test adapter for Django ORM."""

from django.test import TestCase

from ..django_storage import DjangoStorage
from notes import models as notes_models
from notes import entities as notes_entities

storage = DjangoStorage()


class SaveNoteTestCase(TestCase):
    def test_save_note(self):
        note = notes_entities.Note(title='title', body='body')

        note = storage.save_note(note)
        note = notes_models.Note.objects.get(id=note.id)
