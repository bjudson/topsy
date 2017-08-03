"""Domain objects used by the notes app.

Entity classes map to Django models, but have no dependency on an ORM. Use cases exclusively deal in
entities, which allows the business logic to be completely decoupled from the storage layer. The
storage adapter is responsible for converting entities to and from the objects used by the storage
backend, eg Django model instances.

Entity objects are immutable, but have a convenience method Entity.replace() which returns a new
copy of the object, with modified attributes. This is very similar to the Namedtuple._replace()
method:
>>> note = Note(title='Important note', body='TBD', id=1)
>>> note2 = note.replace(title='Important note', body='my_p4ssw0rd')
>>> note
Note(title='Important note', body='TBD', id=1, board_id=None, created_by=None, ...)
>>> note2
Note(title='Important note', body='my_p4ssw0rd', id=1, board_id=None, created_by=None, ...)

We use the attrs package to construct simple, readable entity classes: "All attrs does is take your
declaration, write dunder methods based on that information, and attach them to your class."
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
