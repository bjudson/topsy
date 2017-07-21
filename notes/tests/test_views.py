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
from notes.views import create_board, get_note, edit_note, add_user_to_board


class CreateBoardTestCase(TestCase):
    def setUp(self):
        self.req_factory = RequestFactory()
        self.user = model_factories.User()

    def create_request(self, data):
        request = self.req_factory.post(
            reverse('create_board'),
            content_type='application/json',
            data=json.dumps(data),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user
        request.session = {}
        return request

    def test_create_board_success(self):
        name = 'Sprints'
        request = self.create_request({'name': name})
        response = create_board(request)

        self.assertEqual(response.status_code, 200,
                         'Error: {}'.format(response.content))

        response_data = json.loads(response.content.decode('utf8'))
        self.assertEqual(response_data['board']['name'], name)


class AddUserToBoardTestCase(TestCase):
    def setUp(self):
        self.req_factory = RequestFactory()

    def create_request(self, data, user=None):
        request = self.req_factory.post(
            reverse('add_user_to_board'),
            content_type='application/json',
            data=json.dumps(data),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = user or AnonymousUser()
        request.session = {}
        return request

    def test_add_user_to_board(self):
        board = model_factories.Board()
        owner = model_factories.User(email='bob@blacklodge.net')
        model_factories.BoardUser(user=owner, board=board, role='owner')
        user = model_factories.User(email='mike@blacklodge.net')
        request = self.create_request(
            {
                'user_id': user.id,
                'board_id': board.id,
                'role': 'editor'
            },
            user=owner)
        response = add_user_to_board(request)

        self.assertEqual(response.status_code, 200,
                         'Error: {}'.format(response.content))
        response_data = json.loads(response.content.decode('utf8'))
        self.assertEqual(response_data['board']['name'], board.name)

    def test_no_permission_to_add_user_to_board(self):
        board = model_factories.Board()
        req_user = model_factories.User(email='bob@blacklodge.net')
        user = model_factories.User()
        request = self.create_request({
            'user_id': user.id,
            'board_id': board.id,
            'role': 'editor'
        }, req_user)
        response = add_user_to_board(request)

        self.assertEqual(
            response.status_code, 403,
            'User lacking permissions to add user to board did not recieve error'
        )


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

        self.assertEqual(response.status_code, 200,
                         'Error: {}'.format(response.content))
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

        self.assertEqual(response.status_code, 200,
                         'Error: {}'.format(response.content))
        self.assertEqual(response_data['note']['title'], data['title'])
