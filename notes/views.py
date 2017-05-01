"""
Views for the Notes app are interfaces to use cases dealing with content manipulation.

View functions are what we might consider user-facing HTTP adapters. We avoid putting any business
logic here, but also avoid reliance on Django models. They are in charge of validating user input,
formatting responses, and routing the requests to use cases.
"""

import json

from django.http import JsonResponse

from adapters.django_storage import DjangoStorage
from .use_cases import NoteUseCases

use_cases = NoteUseCases(DjangoStorage())


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
            },
            status_code=400
        )

    if title is not None:
        note = note.replace(title=title)

    if body is not None:
        note = note.replace(body=body)

    note = use_cases.save_note(note)
    return JsonResponse({'note': note.asdict()})
