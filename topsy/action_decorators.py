"""Actions wrap use cases with permission checking and event logging behaviors."""

from functools import wraps
from django.utils.decorators import available_attrs

from topsy.permissions import PermissionError

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


def log(action_name):
    """Decorator to apply to action methods to log action calls."""

    def decorator(method, action_name=action_name):
        @wraps(method, assigned=available_attrs(method))
        def _wrapped_method(self, *args, **kwargs):
            # action_name: kwarg1=val1, kwarg2=val2
            self.logging.info('{}: {}'.format(action_name, ', '.join(
                ['{}={}'.format(k, v) for k, v in kwargs.items()])))
            return method(self, *args, **kwargs)

        return _wrapped_method

    return decorator
