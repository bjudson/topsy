"""Actions users may take for notes and boards.

By wrapping use cases in actions, we create a consistent system for checking permissions, 
writing logs, and auditing."""

from topsy.action import permission, PermissionError
from .use_cases import NoteUseCases


class NoteActions():
    def __init__(self, storage):
        self.use_cases = NoteUseCases(storage)

    @permission('add_user')
    def add_user_to_board(self, board_id, user_id, role):
        board = self.use_cases.add_user_to_board(board_id, user_id, role)
        return board
