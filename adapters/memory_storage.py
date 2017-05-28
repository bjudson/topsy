"""
Storage adapter that uses system memory as backend.

Should have same API as database adapter.
"""


class DoesNotExist(Exception):
    """Exception to be raised when an entity is not found in storage."""

    pass


class MemoryStorage():
    """Adapter to use system memory as a storage backend."""

    def __init__(self):
        """Setup dictionaries as stores for each entity type."""
        self.notes = {}
        self.users = {}
        self.DoesNotExist = DoesNotExist

    def create_user(self, user, password):
        """Create user entity."""
        if user.id is None:
            existing_ids = self.users.keys()
            new_id = 1 if len(existing_ids) == 0 else max(existing_ids) + 1
            user = user.replace(id=new_id)

        self.users[user.id] = user
        return user

    def get_user(self, id):
        try:
            return self.users[id]
        except KeyError:
            raise self.DoesNotExist('User {} was not found'.format(id))

    def save_note(self, note):
        """Store note entity."""
        if note.id is None:
            existing_ids = self.notes.keys()
            new_id = 1 if len(existing_ids) == 0 else max(existing_ids) + 1
            note = note.replace(id=new_id)

        self.notes[note.id] = note
        return note

    def get_note(self, id):
        """Retrieve note entity by ID."""
        try:
            return self.notes[id]
        except KeyError:
            raise self.DoesNotExist('Note {} was not found'.format(id))

    def delete_note(self, id):
        try:
            del self.notes[id]
        except KeyError:
            raise self.DoesNotExist('Note {} was not found'.format(id))

        return True
