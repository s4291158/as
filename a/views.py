from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import LandingForm


def index(request):
    context = {
        "form": LandingForm()
    }
    return render(request, 'index.html', context)


@login_required
def profile(request):
    context = {}
    return render(request, 'account/profile.html', context)


@login_required(login_url="/accounts/signup/")
def booking(request):
    context = {
        "form": LandingForm()
    }

    if request.method == 'POST':
        form = LandingForm(request.POST)
        if form.is_valid():
            form.save()
            context["message"] = "success"
        else:
            context["message"] = "fail"

    return render(request, 'booking.html', context)
