"""General purpose views that don't fit within an app."""

from django.shortcuts import render


def homepage(request):
    """Welcome to Topsy..."""
    return render(request, 'homepage.html')
