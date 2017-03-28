"""
Use cases for managing content in Topsy.

The only content type in Topsy is a Note. Notes can be organized into boards, and boards can be
shared with other users. All the use cases for dealing with boards, notes, and permissions live
in this module.
"""
from .entities import Note


class NoteUseCases():
    """Class containing all Note use cases."""

    def __init__(self, storage):
        """Instantiate with a storage instance that defines the persistence layer."""
        self.storage = storage

    def create_note(self, note_dict, user_id, board_id=None):
        """Take a dictionary representing a note, save to DB and return entity."""
        note = Note(
            title=note_dict['title'],
            body=note_dict['body']
        )

        return self.storage.save_note(note)

    def get_note(self, note_id):
        """Return entity instance for a single note."""
        pass

    def edit_note(self, note_dict):
        """
        Change the content or metadata of a note.

        May want to break this into a number of smaller functions.
        """
        pass

    def delete_note(self, note_dict):
        """Permanently delete a note."""
        pass

    def move_note(self, note_id, board_id):
        """Move a note to another board."""
        pass

    def transfer_note(self, note_id, user_id):
        """Transfer a note to another user."""
        pass

    def create_board(self, name):
        """Create a board to group notes."""
        pass

    def get_user_boards(self, user_id):
        """Get metadata for all boards that a given user has access to."""
        pass

    def get_board(self, board_id):
        """Get metadata for a single board."""
        pass

    def get_board_notes(self, board_id):
        """Get all notes within a board."""
        pass

    def add_user_to_board(self, board_id, user_id):
        """Give another user permission to view a board."""
        pass

    def remove_user_from_board(self, board_id, user_id):
        """Revoke another user's permission to view a board."""
        pass
