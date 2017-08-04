"""Functions that encapsulate business logic for the app.

The only content type in Topsy is a Note. Notes can be organized into boards, and boards can be
shared with other users. All the use cases for dealing with boards, notes, and permissions live
in this module.

Use case functions are actually methods on a simple class, which is just used for injecting the
storage dependency (but could be used to inject other dependencies). When retrieving or modifying
stored objects (notes, boards, etc), use cases only operate on entities, which are converted to
and from ORM objects by the storage layer.
"""
from .entities import Note, Board
from topsy.permissions import board_permissions


class NoteUseCases():
    """Class containing all Note use cases."""

    def __init__(self, storage):
        """Instantiate with a storage instance that defines the persistence layer."""
        self.storage = storage

    def create_note(self, note_dict, user_id, board_id=None):
        """Take a dictionary representing a note, save to DB and return entity."""
        if user_id is None:
            raise ValueError('User ID required to create note.')

        if 'title' not in note_dict.keys():
            raise ValueError('Title required to create note.')

        if 'body' not in note_dict.keys():
            raise ValueError('Body required to create note.')

        try:
            note = Note(**note_dict)
        except TypeError:
            raise ValueError('Note initialized with invalid field')

        return self.storage.save_note(note)

    def get_note(self, note_id):
        """Retrieve entity instance for a single note."""
        return self.storage.get_note(id=note_id)

    def edit_note(self, note_id, title=None, body=None):
        """Edit title and/or body of note."""
        note = self.storage.get_note(id=note_id)

        if title is not None:
            note = note.replace(title=title)

        if body is not None:
            note = note.replace(body=body)

        return self.storage.save_note(note)

    def save_note(self, note):
        """Save note instance to data store."""
        return self.storage.save_note(note)

    def delete_note(self, note_id):
        """Permanently delete a note."""
        return self.storage.delete_note(note_id)

    def move_note(self, note_id, board_id):
        """Move a note to another board."""
        pass

    def create_board(self, name, user_id):
        """Create a board to group notes."""
        if user_id is None:
            raise ValueError('User ID required to create board.')
        board = Board(name=name)
        board = self.storage.save_board(board)
        self.add_user_to_board(board.id, user_id, role='owner')
        return board

    def get_user_boards(self, user_id):
        """Get metadata for all boards that a given user has access to."""
        pass

    def get_board(self, board_id):
        """Get metadata for a single board."""
        pass

    def get_board_notes(self, board_id):
        """Get all notes within a board."""
        pass

    def add_user_to_board(self, board_id, user_id, role='reader'):
        """Give another user permission to view a board."""
        if board_id is None:
            raise ValueError('Board ID required to add user to board.')
        if user_id is None:
            raise ValueError('User ID required to add user to board.')
        if role is None or role not in board_permissions.keys():
            raise ValueError('Invalid board role provided: {}'.format(role))

        return self.storage.save_board_user(board_id, user_id, role)

    def remove_user_from_board(self, board_id, user_id):
        """Revoke another user's permission to view a board."""
        pass
