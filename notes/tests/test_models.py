"""Tests for models in the notes module."""

from django.test import TestCase

from ..entities import Note as NoteEntity, Board as BoardEntity
from ..models import Note as NoteModel, Board as BoardModel


class NoteTestCase(TestCase):
    def setUp(self):
        self.entity = NoteEntity(title='title', body='body')

    def test_from_entity(self):
        note = NoteModel.objects.from_entity(self.entity)

        self.assertEqual(note.title, self.entity.title)

    def test_save(self):
        note = NoteModel.objects.from_entity(self.entity)
        note.save()

        self.assertTrue(note.created_at is not None)
        self.assertTrue(note.modified_at is not None)

    def test_to_entity(self):
        note = NoteModel(title='title', body='body')
        entity = note.to_entity()

        self.assertEqual(note.id, entity.id)
        self.assertEqual(note.title, entity.title)


class BoardTestCase(TestCase):
    def setUp(self):
        self.entity = BoardEntity(name='name')

    def test_from_entity(self):
        board = BoardModel.objects.from_entity(self.entity)

        self.assertEqual(board.name, self.entity.name)

    def test_save(self):
        board = BoardModel.objects.from_entity(self.entity)
        board.save()

        self.assertTrue(board.created_at is not None)
        self.assertTrue(board.modified_at is not None)

    def test_to_entity(self):
        board = BoardModel(name='name')
        entity = board.to_entity()

        self.assertEqual(board.id, entity.id)
        self.assertEqual(board.name, entity.name)
