from django.shortcuts import render


def home(request, *args, **kw):
    html = 'index.html'

    return render(request, html, {})
