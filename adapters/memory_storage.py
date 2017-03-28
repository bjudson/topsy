"""
Storage adapter that uses system memory as backend.

Should have same API as database adapter.
"""
import attr


class MemoryStorage():
    """Adapter to use system memory as a storage backend."""

    def __init__(self):
        """Setup dictionaries as stores for each entity type."""
        self.notes = {}

    def save_note(self, note):
        """Store note entity."""
        if note.id is None:
            existing_ids = self.notes.keys()
            new_id = 1 if len(existing_ids) == 0 else max(existing_ids) + 1
            note = attr.assoc(note, id=new_id)

        self.notes[note.id] = note
        return note

    def get_note(self, id):
        """Retrieve note entity by ID."""
        return self.notes[id]
