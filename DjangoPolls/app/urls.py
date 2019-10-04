"""
Definition of urls for polls viewing and voting.
"""

from django.urls import path
from app.models import Poll
import app.views

urlpatterns = [
    # Home page routing
    path('',
        app.views.PollListView.as_view(
            queryset=Poll.objects.order_by('-pub_date')[:5],
            context_object_name='latest_poll_list',
            template_name='app/index.html',),
        name='home'),
    # Routing for a poll page, which use URLs in the form <poll_id>/,
    # where the id number is captured as a group named "pk".
    path('<int:pk>/',
        app.views.PollDetailView.as_view(
            template_name='app/details.html'),
        name='detail'),
    # Routing for <poll_id>/results pages, again using a capture group
    # named pk.
    path('<int:pk>/results/',
        app.views.PollResultsView.as_view(
            template_name='app/results.html'),
        name='results'),
    # Routing for <poll_id>/vote pages, with the capture group named
    # poll_id this time, which becomes an argument passed to the view.
    path('<int:poll_id>/vote/', app.views.vote, name='vote'),
    path('seed', app.views.seed, name='seed'),
]
