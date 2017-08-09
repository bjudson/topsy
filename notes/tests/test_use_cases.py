"""
Tests for use cases in the notes module.

As much as possible we will test use cases with MemoryStorage to enforce independence between the
use cases and the Django ORM.
"""

import unittest

from adapters.memory_storage import MemoryStorage
from notes.use_cases import NoteUseCases
from notes.entities import Note, Board
from accounts.entities import User


def set_up_use_cases():
    return NoteUseCases(MemoryStorage())

class CreateNoteTestCase(unittest.TestCase):
    """Tests for creating a note."""

    def setUp(self):
        self.use_cases = set_up_use_cases()
        self.storage = self.use_cases.storage

    def test_create_simple_note(self):
        """Create a note with just a title and a body."""
        note_dict = {
            'title': 'The First Note',
            'body': 'Some essential information.'
        }
        user_id = 1

        note = self.use_cases.create_note(note_dict, user_id)
        saved_note = self.storage.get_note(note.id)

        self.assertEqual(note_dict['title'], note.title)
        self.assertEqual(note_dict['body'], note.body)
        self.assertEqual(note_dict['title'], saved_note.title)
        self.assertEqual(note_dict['body'], saved_note.body)

    def test_create_note_without_title(self):
        """Should raise value error when creating a note without a title."""
        with self.assertRaises(ValueError):
            self.use_cases.create_note({'body': 'where be the title'}, 1)

    def test_create_note_with_invalid_field(self):
        """Should raise value error when creating a note with invalid field."""
        with self.assertRaises(ValueError):
            self.use_cases.create_note({
                'title': 'good name',
                'body': 'interesting info',
                'bob': 'useful data'
            }, 1)


class GetNoteTestCase(unittest.TestCase):
    """Tests for retrieving a single note."""

    def setUp(self):
        self.use_cases = set_up_use_cases()
        self.storage = self.use_cases.storage
        self.note = Note(title='title', body='body')
        self.note = self.storage.save_note(self.note)

    def test_get_note_by_id(self):
        """Retrieve a single note instance by id."""
        note = self.use_cases.get_note(self.note.id)

        self.assertEqual(self.note.title, note.title)


class SaveNoteTestCase(unittest.TestCase):
    """Tests for editing a single note."""

    def setUp(self):
        self.use_cases = set_up_use_cases()
        self.storage = self.use_cases.storage
        self.note = Note(title='title', body='body')
        self.note = self.storage.save_note(self.note)

    def test_edit_note_title_and_save(self):
        """Edit the title of a note."""
        new_title = 'new title'
        note = self.note.replace(title=new_title)

        self.use_cases.save_note(note)

        new_note = self.storage.get_note(self.note.id)
        self.assertEqual(note, new_note)
        self.assertEqual(new_note.title, new_title)

    def test_edit_note_board_and_save(self):
        """Edit the board for a note."""
        board = Board(name='the best notes')
        board = self.storage.save_board(board)
        note = self.note.replace(board_id=board.id)

        self.use_cases.save_note(note)

        new_note = self.storage.get_note(self.note.id)
        self.assertEqual(note, new_note)
        self.assertEqual(new_note.board_id, board.id)


class MoveNoteTestCase(unittest.TestCase):
    """Tests for moving a note."""

    def setUp(self):
        self.use_cases = set_up_use_cases()
        self.storage = self.use_cases.storage
        self.board = self.storage.save_board(Board(name='mediocre notes'))
        self.note = Note(title='title', body='body', board_id=self.board.id)
        self.note = self.storage.save_note(self.note)

    def test_move_note_success(self):
        """Edit the board for a note."""
        board = Board(name='the best notes')
        board = self.storage.save_board(board)

        self.use_cases.move_note(note_id=self.note.id, board_id=board.id)

        new_note = self.storage.get_note(self.note.id)
        self.assertEqual(new_note.board_id, board.id)


class DeleteNoteTestCase(unittest.TestCase):
    """Tests for deleting a single note."""

    def setUp(self):
        self.use_cases = set_up_use_cases()
        self.storage = self.use_cases.storage
        self.note = Note(title='title', body='body')
        self.note = self.storage.save_note(self.note)

    def test_delete_note_successfully(self):
        """Should be able to delete a note."""
        self.use_cases.delete_note(self.note.id)

        with self.assertRaises(self.storage.DoesNotExist):
            self.storage.get_note(self.note.id)


class CreateBoardTestCase(unittest.TestCase):
    """Tests for creating a board."""

    def setUp(self):
        self.use_cases = set_up_use_cases()
        self.storage = self.use_cases.storage
        self.user = User(id=1, name='Bob', email='bob@subgenius.com')
        self.storage.create_user(self.user, 'sl4ck')

    def test_create_board(self):
        board_name = 'The Stark Fist of Removal'

        board = self.use_cases.create_board(name=board_name, user_id=self.user.id)
        saved_board = self.storage.get_board(board.id)
        board_users = self.storage.get_board_users(board.id)

        self.assertEqual(board_name, board.name)
        self.assertEqual(board_name, saved_board.name)
        self.assertTrue(self.user.id in [u['id'] for u in board_users])


class AddUserToBoardTestCase(unittest.TestCase):
    """Tests for adding board permissions."""

    def setUp(self):
        self.use_cases = set_up_use_cases()
        self.storage = self.use_cases.storage
        self.user = User(id=1, name='Bob', email='bob@subgenius.com')
        self.storage.create_user(self.user, 'sl4ck')

        self.board = Board(id=1, name='The Book of the SubGenius')
        self.storage.save_board(self.board)

    def test_add_user_to_board(self):
        """Adding user to board should create correct join record."""
        self.use_cases.add_user_to_board(
            board_id=self.board.id, user_id=self.user.id, role='editor')

        join = self.storage.board_users[0]

        self.assertEqual(join['user_id'], self.user.id)
        self.assertEqual(join['board_id'], self.board.id)
        self.assertEqual(join['role'], 'editor')

    def test_add_user_to_board_with_invalid_role(self):
        """Using invalid role should raise ValueError."""
        with self.assertRaises(ValueError):
            self.use_cases.add_user_to_board(
                board_id=self.board.id, user_id=self.user.id, role='czar')


class RemoveUserFromBoardTestCase(unittest.TestCase):
    """Tests for removing board permissions."""

    def setUp(self):
        self.use_cases = set_up_use_cases()
        self.storage = self.use_cases.storage

        self.user = User(id=1, name='Bob', email='bob@subgenius.com')
        self.storage.create_user(self.user, 'sl4ck')

        self.board = Board(id=1, name='The Book of the SubGenius')
        self.storage.save_board(self.board)

        self.storage.save_board_user(board_id=self.board.id, user_id=self.user.id, role='owner')

    def test_remove_user_from_board(self):
        """Removing user from board should delete join record."""
        self.use_cases.remove_user_from_board(board_id=self.board.id, user_id=self.user.id)

        with self.assertRaises(IndexError):
            self.storage.board_users[0]


class DeleteBoardTestCase(unittest.TestCase):
    """Tests for deleting boards."""

    def setUp(self):
        self.use_cases = set_up_use_cases()
        self.storage = self.use_cases.storage
        self.user = self.storage.create_user(
            User(name='Bob', email='bob@subgenius.com'),
            'sl4ck'
        )
        self.board = self.storage.save_board(
            Board(name='The Book of the SubGenius')
        )
        self.note = self.storage.save_note(
            Note(title='Stark fist of removal', body='...', board_id=self.board.id)
        )

        self.storage.save_board_user(user_id=self.user.id, board_id=self.board.id, role='owner')

    def test_delete_board_success(self):
        """Deleting board should delete its notes & joins to users."""
        self.use_cases.delete_board(board_id=self.board.id)

        users = [bu for bu in self.storage.board_users if bu['board_id'] == self.board.id]
        self.assertEqual(len(users), 0)

        with self.assertRaises(self.storage.DoesNotExist):
            self.storage.get_board(id=self.board.id)

        with self.assertRaises(self.storage.DoesNotExist):
            self.storage.get_note(id=self.note.id)


if __name__ == '__main__':
    unittest.main(verbosity=2)
