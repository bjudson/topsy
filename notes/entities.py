"""
Domain objects used by the notes app.

These classes map to Django models, but have no dependency on an ORM. We use the attrs package to
construct simple, readable entity classes: "All attrs does is take your declaration, write dunder
methods based on that information, and attach them to your class."
"""

import attr
from datetime import datetime

from topsy.entities import Entity


@attr.s(frozen=True)
class Note(Entity):
    """Notes are where users put the useful knowledge they need to save & share."""

    title = attr.ib()
    body = attr.ib()
    id = attr.ib(default=None)
    board_id = attr.ib(default=None)
    created_by = attr.ib(default=None)
    created_at = attr.ib(default=datetime.utcnow())
    modified_at = attr.ib(default=datetime.utcnow())
    status = attr.ib(default='active')


@attr.s(frozen=True)
class Board(Entity):
    """Boards are where users put their many useful notes."""

    name = attr.ib()
    id = attr.ib(default=None)
    created_at = attr.ib(default=datetime.utcnow())
    modified_at = attr.ib(default=datetime.utcnow())
    status = attr.ib(default='active')
