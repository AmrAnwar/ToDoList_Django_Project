from django.shortcuts import render, get_object_or_404, redirect


def index(request):
    """
    render home page
    """
    return render(request, "base.html")
