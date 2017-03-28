"""The value objects used by the notes app."""

import attr
from datetime import datetime


@attr.s(frozen=True)
class Note():
    """An object that represents a container for notes."""

    title = attr.ib()
    body = attr.ib()
    id = attr.ib(default=None)
    board_id = attr.ib(default=None)
    created_by = attr.ib(default=None)
    created_at = attr.ib(default=datetime.utcnow())
    modified_at = attr.ib(default=datetime.utcnow())
    status = attr.ib(default='active')


@attr.s(frozen=True)
class Board():
    """An object that represents a container for notes."""

    name = attr.ib()
    id = attr.ib(default=None)
    created_at = attr.ib(default=datetime.utcnow())
    modified_at = attr.ib(default=datetime.utcnow())
    status = attr.ib(default='active')
