"""
Adapter for Django ORM.

Pretty much all calls to the database in the live app should go through the methods of this class.
The MemoryStorage class shares the same interface, but doesn't depend on an actual database. It can
be swapped out for this one when testing use cases.
"""

from accounts import models as accounts_models
from notes import models as notes_models


class DoesNotExist(Exception):
    """Exception to be raised when an entity is not found in storage."""

    pass


class DjangoStorage():
    """Adapter to use Django ORM as a storage backend."""

    DoesNotExist = DoesNotExist

    def __init__(self):
        """Setup dictionaries as stores for each entity type."""
        self.notes = {}

    def create_user(self, user, password):
        """Create user entity.

        Because Django provides password hashing functionality that we want to use, we perform this
        action in the adapter, so that nothing is imported from Django in our use case.
        """
        django_user = accounts_models.User.objects.from_entity(user)
        django_user.set_password(password)
        django_user.save()
        return django_user.to_entity()

    def save_board(self, board):
        """Store board entity."""
        django_board = notes_models.Board.objects.from_entity(board)
        django_board.save()
        return django_board.to_entity()

    def save_board_user(self, board_id, user_id, role):
        """Give user access to a board, or change user's role on board."""
        board_user = notes_models.BoardUser.objects.create(
            board_id=board_id, user_id=user_id, role=role)
        return board_user.board.to_entity()

    def get_role(self, user_id, board_id):
        """Get user's role on a board. Returns none if user is not on board."""
        try:
            rel = notes_models.BoardUser.objects.get(user_id=user_id, board_id=board_id)
        except notes_models.BoardUser.DoesNotExist:
            return None
        return rel.role

    def save_note(self, note):
        """Store note entity."""
        django_note = notes_models.Note.objects.from_entity(note)
        django_note.save()
        return django_note.to_entity()

    def get_note(self, id):
        """Retrieve note entity by ID."""
        try:
            django_note = notes_models.Note.objects.get(id=id)
        except notes_models.Note.DoesNotExist:
            raise self.DoesNotExist('Note {} was not found.'.format(id))

        return django_note.to_entity()

    def delete_note(self, id):
        """Permanently delete note by ID."""
        try:
            django_note = notes_models.Note.objects.get(id=id)
        except notes_models.Note.DoesNotExist:
            raise self.DoesNotExist('Note {} was not found.'.format(id))

        return django_note.delete()
