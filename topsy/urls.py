"""All URLs for the project go here."""
from django.conf.urls import url
from topsy import views as topsy_views
from accounts import views as accounts_views
from notes import views as notes_views

urlpatterns = [
    url(r'^$', topsy_views.homepage, name='homepage'),

    # Accounts
    url(r'^accounts/create/$', accounts_views.create_account, name='create_account'),
    url(r'^accounts/login/$', accounts_views.login, name='login'),
    url(r'^logout/$', accounts_views.logout, name='logout'),

    # Notes & Boards
    url(r'^notes/(?P<note_id>[0-9]+)/$', notes_views.get_note, name='get_note'),
    url(r'^notes/edit/$', notes_views.edit_note, name='edit_note'),
    url(r'^boards/create/$', notes_views.create_board, name='create_board'),
    url(r'^boards/add-user/$', notes_views.add_user_to_board, name='add_user_to_board')
]
