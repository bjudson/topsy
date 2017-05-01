"""
Base classes for value objects used in Topsy.

We use the attrs package to reduce boilerplate for all Topsy entities: "All attrs does is take
your declaration, write dunder methods based on that information, and attach them to your class."
"""

import attr


class Entity():
    """
    Base class for all Topsy entities.

    Attaches attrs helper methods for convenience, and so that our business logic doesn't need to
    rely on attrs directly.
    """

    def replace(self, **kwargs):
        """Return new instance of this entity with updated field."""
        return attr.assoc(self, **kwargs)

    def asdict(self):
        """Return class attributes in a dictionary."""
        return attr.asdict(self)
