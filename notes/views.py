"""
Views for the Notes app are interfaces to use cases dealing with content manipulation.

View functions are what we might consider user-facing HTTP adapters. We avoid putting any business
logic here, but also avoid reliance on Django models. They are in charge of validating user input,
formatting responses, and routing the requests to use cases.
"""

import json

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from adapters.django_storage import DjangoStorage
from adapters.django_logging import django_logging
from .use_cases import NoteUseCases
from .actions import NoteActions, PermissionError
from topsy.permission_checker import PermissionChecker

storage = DjangoStorage()
use_cases = NoteUseCases(storage)
actions = NoteActions(storage, django_logging)
get_perms = PermissionChecker(storage)


@login_required
def create_board(request):
    """Create a new board."""
    req_data = json.loads(request.body.decode('utf8'))
    name = req_data.get('name')

    board = use_cases.create_board(name=name, user_id=request.user.id)

    return JsonResponse({'board': board.asdict()})


@login_required
def add_user_to_board(request):
    """Create a new board."""
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
        return JsonResponse({'error': str(e)}, status=403)

    return JsonResponse({'board': board.asdict()})


def get_note(request, note_id):
    """Display an individual note."""
    note = use_cases.get_note(note_id)
    return JsonResponse({'note': note.asdict()})


def edit_note(request):
    """Use JSON data attached to request to edit content/metadata of individual note."""
    req_data = json.loads(request.body.decode('utf8'))
    note_id = req_data.get('id')
    title = req_data.get('title')
    body = req_data.get('body')

    try:
        note = use_cases.get_note(note_id)
    except DjangoStorage.DoesNotExist:
        return JsonResponse(
            {
                'success': False,
                'message': 'Note {} does not exist'.format(note_id)
            }, status=400)
    if title is not None:
        note = note.replace(title=title)

    if body is not None:
        note = note.replace(body=body)

    note = use_cases.save_note(note)
    return JsonResponse({'note': note.asdict()})
