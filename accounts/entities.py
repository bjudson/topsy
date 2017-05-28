"""
Domain objects used by the accounts app.

These classes map to Django models, but have no dependency on an ORM. We use the attrs package to
construct simple, readable entity classes: "All attrs does is take your declaration, write dunder
methods based on that information, and attach them to your class."
"""

import attr
from datetime import datetime

from topsy.entities import Entity


@attr.s(frozen=True)
class User(Entity):
    """User is the object identifying each person who has signed up for Topsy."""

    email = attr.ib()
    name = attr.ib()
    id = attr.ib(default=None)
    created_at = attr.ib(default=datetime.utcnow())
    modified_at = attr.ib(default=datetime.utcnow())
    is_active = attr.ib(default=True)
    is_admin = attr.ib(default=False)
    last_login = attr.ib(default=None)
    status = attr.ib(default='active')
