"""
Contains all business logic for managing user account data (authentication, settings, etc).

Billing information and subscriptions are handled by the payments app.
"""
from .entities import User


class AccountUseCases():
    """Class containing all use cases for User accounts."""

    def __init__(self, storage):
        """Instantiate with a storage instance that defines the persistence layer."""
        self.storage = storage

    def create_account(self, user_dict, password):
        """Create new user account."""
        user = User(**user_dict)

        return self.storage.create_user(user, password)

    def edit_account(self, email, name):
        """Change email and name for an individual user."""
        pass

    def deactivate(self, user_id):
        """Deactivate user's account."""
        pass
