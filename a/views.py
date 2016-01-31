from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    context = {}
    return render(request, 'index.html', context)


@login_required
def profile(request):
    context = {}
    return render(request, 'account/profile.html', context)
