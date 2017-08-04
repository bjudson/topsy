"""Actions users may take for notes and boards.

By wrapping use cases in actions, we create a consistent system for checking permissions, 
writing logs, and auditing."""

from topsy.action_decorators import permission, log
from .use_cases import NoteUseCases


class NoteActions():
    def __init__(self, storage, logging):
        self.use_cases = NoteUseCases(storage)
        self.logging = logging

    @permission('add_user')
    @log('board.add_user')
    def add_user_to_board(self, board_id, user_id, role):
        board = self.use_cases.add_user_to_board(board_id, user_id, role)
        return board
