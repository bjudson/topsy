from django.conf.urls import url
from accounts import views as accounts_views
from notes import views as notes_views

urlpatterns = [
    # Accounts
    url(r'^accounts/create/', accounts_views.create_account, name='create_account'),

    # Notes
    url(r'^notes/(?P<note_id>[0-9]+)/', notes_views.get_note, name='get_note'),
    url(r'^notes/edit/', notes_views.edit_note, name='edit_note'),
]
