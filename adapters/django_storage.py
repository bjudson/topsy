"""
Adapter for Django ORM.

Pretty much all calls to the database in the live app should go through the methods of this class.
"""

from notes import models as notes_models


class DoesNotExist(Exception):
    """Exception to be raised when an entity is not found in storage."""

    pass


class DjangoStorage():
    """Adapter to use system memory as a storage backend."""

    def __init__(self):
        """Setup dictionaries as stores for each entity type."""
        self.notes = {}
        self.DoesNotExist = DoesNotExist

    def save_note(self, note):
        """Store note entity."""
        django_note = notes_models.Note.objects.from_entity(note)
        django_note.save()
        return django_note.to_entity()

    def get_note(self, id):
        """Retrieve note entity by ID."""
        pass

    def delete_note(self, id):
        """Permanently delete note by ID."""
        pass
