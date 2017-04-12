"""Base classes for value objects used in Topsy."""

import attr


class Entity():
    """Base class for all Topsy entities."""

    def replace(self, field, value):
        """Return new instance of this entity with updated field."""
        return attr.assoc(self, **{field: value})
