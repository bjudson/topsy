"""Interface for checking a given user's permissions on a given board."""

board_permissions = {
    'reader': ('view_notes', ),
    'editor': ('view_notes', 'add_note', 'delete_note', 'edit_note'),
    'owner': ('view_notes', 'add_note', 'delete_note', 'edit_note', 'add_user', 'remove_user',
              'edit_name', 'delete')
}


class PermissionChecker():
    """Check user's permissions on a board.

    Examples:
    >>> get_perms = PermissionChecker(DjangoStorage())
    >>> get_perms(user_id, board_id)
    ('view_notes', 'add_note', 'delete_note', 'edit_note')

    >>> get_perms = PermissionChecker(DjangoStorage())
    >>> get_perms(user_id, board_id, 'edit_note')
    True
    """

    def __init__(self, storage):
        self._storage = storage

    def __call__(self, user_id, board_id, permission_required=None):
        permissions = self._get_permissions(user_id, board_id)
        if permission_required:
            return permission_required in permissions
        return permissions

    def _get_permissions(self, user_id, board_id):
        role = self._storage.get_role(user_id=user_id, board_id=board_id)
        if role is None:
            return []
        return board_permissions[role]
