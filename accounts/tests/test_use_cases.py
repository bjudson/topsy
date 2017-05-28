"""
Tests for use cases in the accounts module.

As much as possible we will test use cases with MemoryStorage to enforce independence between the
use cases and the Django ORM.
"""

import unittest

from adapters.memory_storage import MemoryStorage
from accounts.use_cases import AccountUseCases

storage = MemoryStorage()
use_cases = AccountUseCases(storage)


class CreateAccountTestCase(unittest.TestCase):
    """Tests for creating user account."""

    def test_create_account(self):
        """Basic successful account creation."""
        user_dict = {
            'name': 'Bob',
            'email': 'bob@subgenius.com',
        }

        user = use_cases.create_account(user_dict=user_dict, password='sl4ck')
        saved_user = storage.get_user(user.id)

        self.assertEqual(user_dict['name'], saved_user.name)
        self.assertEqual(user_dict['email'], saved_user.email)
