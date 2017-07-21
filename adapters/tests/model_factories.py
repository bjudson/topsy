"""Factory Boy classes used for test fixtures."""

import factory


class User(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.User'

    name = 'User'
    email = 'user@example.com'


class Note(factory.django.DjangoModelFactory):
    class Meta:
        model = 'notes.Note'

    title = 'Title'
    body = 'Body...'


class Board(factory.django.DjangoModelFactory):
    class Meta:
        model = 'notes.Board'

    name = 'Board'


class BoardUser(factory.django.DjangoModelFactory):
    class Meta:
        model = 'notes.BoardUser'
