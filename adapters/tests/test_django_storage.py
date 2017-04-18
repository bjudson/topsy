"""Test adapter for Django ORM."""

from django.test import TestCase

from ..django_storage import DjangoStorage
from notes import models as notes_models
from notes import entities as notes_entities
from . import model_factories

storage = DjangoStorage()


class SaveNoteTestCase(TestCase):
    """Tests for saving notes."""

    def test_save_note(self):
        note = notes_entities.Note(title='title', body='body')

        note = storage.save_note(note)

        saved_note = notes_models.Note.objects.get(id=note.id)
        self.assertEqual(note.title, saved_note.title)


class GetNoteTestCase(TestCase):
    """Tests for retrieving notes."""

    def test_get_note(self):
        note = model_factories.Note.create()

        saved_note = storage.get_note(note.id)

        self.assertEqual(note.id, saved_note.id)

    def test_not_found_exception(self):
        with self.assertRaises(storage.DoesNotExist):
            storage.get_note(id=5000)


class DeleteNoteTestCase(TestCase):
    """Tests for deleting notes."""

    def test_delete_note(self):
        note = model_factories.Note.create()

        storage.delete_note(note.id)

        with self.assertRaises(storage.DoesNotExist):
            storage.get_note(id=note.id)
