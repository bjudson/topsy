"""Actions wrap use cases with permission checking and event logging behaviors."""

from functools import wraps
from django.utils.decorators import available_attrs


class PermissionError(Exception):
    pass


def permission(permission_required):
    """Decorator to apply to action methods to check permissions."""

    def decorator(method, permission_required=permission_required):
        @wraps(method, assigned=available_attrs(method))
        def _wrapped_method(self, *args, **kwargs):
            permissions = kwargs.pop('permissions')
            if permission_required in permissions:
                return method(self, *args, **kwargs)

            raise PermissionError('User lacks permission: {}'.format(permission_required))

        return _wrapped_method

    return decorator
