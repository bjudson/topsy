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
        self.boards = {}
        self.users = {}
        self.board_users = []
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

    def save_board(self, board):
        """Store board entity."""
        if board.id is None:
            existing_ids = self.boards.keys()
            new_id = 1 if len(existing_ids) == 0 else max(existing_ids) + 1
            board = board.replace(id=new_id)

        self.boards[board.id] = board
        return board

    def save_board_user(self, board_id, user_id, role):
        """Give user access to a board, or change user's role on board."""
        for board_user in self.board_users:
            if board_user['board_id'] == board_id and board_user['user_id'] == user_id:
                board_user['role'] = role
                return board_user

        record = {
            'board_id': board_id,
            'user_id': user_id,
            'role': role
        }

        self.board_users.append(record)

        return record

    def delete_board_user(self, board_id, user_id):
        for key, board_user in enumerate(self.board_users):
            if board_user['board_id'] == board_id and board_user['user_id'] == user_id:
                bu = self.board_users.pop(key)
                return bu

        raise ValueError('User {} not joined to board {}.'.format(board_id, user_id))

    def get_board(self, id):
        """Retrieve board entity by ID."""
        if type(id) is not int:
            raise ValueError('Board id must be integer, not {}'.format(type(id).__name__))

        try:
            return self.boards[id]
        except KeyError:
            raise self.DoesNotExist('Board {} was not found'.format(id))

    def get_board_users(self, id):
        """Return list of users who have access to board."""
        users = []
        user_roles = [(bu['user_id'], bu['role'])
                      for bu in self.board_users if bu['board_id'] == id]

        for role in user_roles:
            for u in self.users.values():
                if u.id == role[0]:
                    users.append({
                        'id': u.id,
                        'name': u.name,
                        'email': u.email,
                        'role': role[1]
                    })

        return users

    def get_role(self, user_id, board_id):
        for bu in self.board_users:
            if bu['board_id'] == board_id and bu['user_id'] == user_id:
                return bu['role']

        return None

    def get_board_notes(self, id):
        return [note for note in self.notes.values() if note.board_id == id]

    def delete_board(self, id):
        return self.boards.pop(id)
