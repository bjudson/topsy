"""Test action decorators."""

import unittest

from ..action_decorators import permission, log, PermissionError
from adapters.memory_logging import MemoryLogging


class PermissionTestCase(unittest.TestCase):
    @permission('see_the_future')
    def future_python(self):
        return 'Strict type system!'

    def test_permission_pass(self):
        future = self.future_python(permissions=('see_the_future', ))
        self.assertIsNotNone(future)

    def test_permission_fail(self):
        with self.assertRaises(PermissionError):
            self.future_python(permissions=('see_the_past', ))


class LogTestCase(unittest.TestCase):
    def setUp(self):
        self.logging = MemoryLogging()

    @log('board.add_user')
    def add_user_to_board(self, user_id, board_id, role):
        return True

    def test_log(self):
        result = self.add_user_to_board(user_id=1, board_id=1, role='editor')
        self.assertTrue('editor' in self.logging.dump()[0][1], self.logging.dump()[0])
        self.assertEqual(result, True)
