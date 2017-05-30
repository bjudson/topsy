"""
Tests for views.

These tend to be integration tests that make sure views return correct data (or the correct errors).
They don't need to be very detailed. But they will test that view, use case, models, and entities
are all playing nicely together.
"""

import json
from unittest.mock import MagicMock

from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser

from accounts.models import User as UserModel
from accounts.views import create_account, login


class CreateAccountTestCase(TestCase):
    def setUp(self):
        self.req_factory = RequestFactory()

    def create_request(self, data):
        request = self.req_factory.post(
            reverse('create_account'),
            content_type='application/json',
            data=json.dumps(data),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = AnonymousUser()
        request.session = {}
        return request

    def test_create_account_success(self):
        user_dict = {
            'name': 'Bob',
            'email': 'bob@subgenius.com',
            'password': 'sl4ck'
        }

        request = self.create_request(user_dict)
        response = create_account(request)
        response_data = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 200, 'Error: {}'.format(response.content))
        self.assertEqual(response_data['user']['email'], user_dict['email'])

    def test_create_account_missing_data(self):
        user_dict = {
            'name': 'Bob',
            'email': 'bob@subgenius.com',
            # No password submitted
        }

        request = self.create_request(user_dict)
        response = create_account(request)
        response_data = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 400, 'Error: {}'.format(response.content))
        self.assertEqual(response_data['success'], False)
        self.assertTrue('password' in response_data['message'])


class LoginTestCase(TestCase):
    def setUp(self):
        self.req_factory = RequestFactory()
        self.user = UserModel(email='bob@subgenius.com', name='Bob')
        self.user.set_password('sl4ck')
        self.user.save()

    def create_request(self, data):
        request = self.req_factory.post(
            reverse('login'),
            content_type='application/json',
            data=json.dumps(data),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = AnonymousUser()
        request.session = MagicMock()
        return request

    def test_login_success(self):
        credentials = {
            'email': 'bob@subgenius.com',
            'password': 'sl4ck'
        }

        request = self.create_request(credentials)
        response = login(request)
        response_data = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 200, 'Response: {}'.format(response.content))
        self.assertEqual(response_data['user']['email'], credentials['email'])

    def test_login_bad_password(self):
        credentials = {
            'email': 'bob@subgenius.com',
            'password': 'slack'  # Incorrect password
        }

        request = self.create_request(credentials)
        response = login(request)

        self.assertEqual(response.status_code, 400, 'Response: {}'.format(response.content))
