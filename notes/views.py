"""Views for the Notes app are interfaces to use cases dealing with content manipulation.

View functions are what we might consider user-facing HTTP adapters. We avoid putting any business
logic here, but also avoid reliance on Django models. They are in charge of validating user input,
formatting responses, and routing the requests to use cases.
"""

import json

from django.contrib.auth.decorators import login_required

from topsy.utils import json_success, json_error
from adapters.django_storage import DjangoStorage
from adapters.django_logging import django_logging
from .use_cases import NoteUseCases
from .actions import NoteActions
from topsy.permissions import PermissionChecker, PermissionError

storage = DjangoStorage()
use_cases = NoteUseCases(storage)
actions = NoteActions(storage, django_logging)
get_perms = PermissionChecker(storage)


@login_required
def create_board(request):
    """Create a new board."""
    req_data = json.loads(request.body.decode('utf8'))
    try:
        name = req_data['name']
    except KeyError:
        return json_error('Board name is required')

    board = actions.create_board(name=name, user_id=request.user.id)

    return json_success({'board': board.asdict()})


@login_required
def delete_board(request):
    req_data = json.loads(request.body.decode('utf8'))
    try:
        board_id = req_data['id']
    except KeyError:
        return json_error('Board id is required')

    try:
        board = actions.delete_board(
            id=board_id,
            permissions=get_perms(request.user.id, board_id)
        )
    except PermissionError as e:
        return json_error(str(e), status=403)

    return json_success({'board': board.asdict()})


@login_required
def add_user_to_board(request):
    """Add user to a board."""
    req_data = json.loads(request.body.decode('utf8'))
    user_id = req_data.get('user_id')
    board_id = req_data.get('board_id')
    role = req_data.get('role')

    try:
        board = actions.add_user_to_board(
            user_id=user_id,
            board_id=board_id,
            role=role,
            permissions=get_perms(request.user.id, board_id))
    except PermissionError as e:
        return json_error(str(e), status=403)

    return json_success({'board': board.asdict()})


@login_required
def remove_user_from_board(request):
    """Remove user from a board."""
    req_data = json.loads(request.body.decode('utf8'))
    user_id = req_data.get('user_id')
    board_id = req_data.get('board_id')

    try:
        board_user = actions.remove_user_from_board(
            user_id=user_id,
            board_id=board_id,
            permissions=get_perms(request.user.id, board_id))
    except PermissionError as e:
        return json_error(str(e), status=403)

    return json_success({'board_user': board_user})

@login_required
def get_note(request, note_id):
    """Display an individual note."""

    try:
        note = storage.get_note(note_id)
        note = actions.get_note(note_id, permissions=get_perms(request.user.id, note.board_id))
    except DjangoStorage.DoesNotExist:
        return json_error('Note {} does not exist'.format(note_id))
    except PermissionError as e:
        return json_error(str(e), status=403)

    return json_success({'note': note.asdict()})


@login_required
def edit_note(request):
    """Edit content/metadata of individual note."""
    req_data = json.loads(request.body.decode('utf8'))
    try:
        note_id = req_data['id']
    except KeyError:
        return json_error('Note id is required')

    title = req_data.get('title')
    body = req_data.get('body')

    try:
        note = storage.get_note(note_id)
        note = actions.edit_note(
            note_id,
            title=title,
            body=body,
            permissions=get_perms(request.user.id, note.board_id)
        )
    except DjangoStorage.DoesNotExist:
        return json_error('Note {} does not exist'.format(note_id))
    except PermissionError as e:
        return json_error(str(e), status=403)

    return json_success({'note': note.asdict()})
