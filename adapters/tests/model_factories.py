"""Factory Boy classes used for test fixtures."""

import factory


class Note(factory.django.DjangoModelFactory):
    class Meta:
        model = 'notes.Note'

    title = 'Title'
    body = 'Body...'
