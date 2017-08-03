"""Functions that encapsulate business logic for the app.

Accounts app contains use cases for account managment, eg creating account, changing password,
changing email, etc.

Use case functions are actually methods on a simple class, which is just used for injecting the
storage dependency (but could be used to inject other dependencies). When retrieving or modifying
stored objects (users), use cases only operate on entities, which are converted to and from ORM
objects by the storage layer.
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
        """Change email and/or name for an individual user."""
        pass

    def change_password(self, user_id, new_password):
        """Change email and/or name for an individual user."""
        pass

    def deactivate(self, user_id):
        """Deactivate user's account."""
        pass
