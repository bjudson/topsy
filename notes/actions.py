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

    @permission('add_user')
    @log('board.add_user')
    def add_user_to_board(self, board_id, user_id, role):
        return self.use_cases.add_user_to_board(board_id, user_id, role)
