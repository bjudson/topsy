"""
Tests for use cases in the notes module.

As much as possible we will test use cases with MemoryStorage to enforce independence between the
use cases and the Django ORM.
"""

import unittest

from adapters.memory_storage import MemoryStorage
from notes.use_cases import NoteUseCases

storage = MemoryStorage()
use_cases = NoteUseCases(storage)


class CreateNoteTestCase(unittest.TestCase):
    """Tests for creating a note."""

    def test_create_simple_note(self):
        """Create a note with just a title and a body."""
        note_dict = {
            'title': 'The First Note',
            'body': 'Some essential information.'
        }
        user_id = 1

        note = use_cases.create_note(note_dict, user_id)
        saved_note = storage.get_note(note.id)

        self.assertEqual(note_dict['title'], note.title)
        self.assertEqual(note_dict['body'], note.body)
        self.assertEqual(note_dict['title'], saved_note.title)
        self.assertEqual(note_dict['body'], saved_note.body)

if __name__ == '__main__':
    unittest.main(verbosity=2)
