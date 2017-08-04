"""Actions users may take on notes and boards.

These are just wrapper methods around use cases, which allow us to consistently apply side effect
behavior to actions performaned by users. The examples we show are decorators for logging
transation data and checking permissions on a per-action basis.
"""

from topsy.action_decorators import permission, log
from .use_cases import NoteUseCases


class NoteActions():
    def __init__(self, storage, logging):
        self.use_cases = NoteUseCases(storage)
        self.logging = logging

    # Anyone can create a board anytime, no permissions required
    @log('board.create')
    def create_board(self, name, user_id):
        return self.use_cases.create_board(name, user_id)

    # We're not going to log every view request, but we will check permissions
    @permission('view_notes')
    def get_board(self, board_id):
        return self.use_cases.get_board(board_id)

    @permission('view_notes') # Permissions should be for parent board object
    def get_note(self, note_id):
        return self.use_cases.get_note(note_id)

    @permission('view_notes') # Permissions should be for parent board object
    @log('note.edit')
    def edit_note(self, note_id, title=None, body=None):
        return self.use_cases.edit_note(note_id, title=title, body=body)

    # Adding user to a board requires permissions, and we want to log the transaction
    @permission('add_user')
    @log('board.add_user')
    def add_user_to_board(self, board_id, user_id, role):
        # Could have other side effects here, like sending a notification to the user added
        return self.use_cases.add_user_to_board(board_id, user_id, role)
