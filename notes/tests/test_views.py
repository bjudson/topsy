"""
Tests for views.

These tend to be integration tests that make sure views return correct data (or the correct errors).
They don't need to be very detailed. But they will test that view, use case, models, and entities
are all playing nicely together.
"""

import json

from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser

from adapters.tests import model_factories
from notes.views import create_board, get_note, edit_note


class CreateBoardTestCase(TestCase):
    def setUp(self):
        self.req_factory = RequestFactory()

    def create_request(self, data):
        request = self.req_factory.post(
            reverse('create_board'),
            content_type='application/json',
            data=json.dumps(data),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = AnonymousUser()
        request.session = {}
        return request

    def test_create_board_success(self):
        name = 'Sprints'
        request = self.create_request({'name': name})
        response = create_board(request)
        response_data = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 200, 'Error: {}'.format(response.content))
        self.assertEqual(response_data['board']['name'], name)


class GetNoteTestCase(TestCase):
    def setUp(self):
        self.req_factory = RequestFactory()

    def create_request(self, id):
        request = self.req_factory.get(
            reverse('get_note', args=[id]),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = AnonymousUser()
        request.session = {}
        return request

    def test_get_note(self):
        note = model_factories.Note()

        request = self.create_request(note.id)
        response = get_note(request, note.id)
        response_data = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 200, 'Error: {}'.format(response.content))
        self.assertEqual(response_data['note']['id'], note.id)


class EditNoteTestCase(TestCase):
    def setUp(self):
        self.req_factory = RequestFactory()

    def create_request(self, data=None):
        request = self.req_factory.post(
            reverse('edit_note'),
            content_type='application/json',
            data=json.dumps(data),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = AnonymousUser()
        request.session = {}
        return request

    def test_save_note(self):
        note = model_factories.Note(title='original title')

        data = {'id': note.id, 'title': 'new title'}
        request = self.create_request(data)
        response = edit_note(request)
        response_data = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 200, 'Error: {}'.format(response.content))
        self.assertEqual(response_data['note']['title'], data['title'])
