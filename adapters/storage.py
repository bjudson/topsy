"""Contains shared classes for storage adapters, including abstract base class."""

import abc

class DoesNotExist(Exception):
    """Exception to be raised when an entity is not found in storage."""
    pass

class Storage(abc.ABC):
    """Base class for storage adapters."""
    DoesNotExist = DoesNotExist

    @abc.abstractmethod
    def create_user(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def save_board(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def save_board_user(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_role(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def save_note(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_note(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def delete_note(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_board(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_board_notes(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_board_users(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def delete_board_user(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def delete_board(self, *args, **kwargs):
        pass
