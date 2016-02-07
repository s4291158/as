from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from allauth.account.views import SignupView

from .forms import LandingForm, BookingForm

from urllib import parse


def index(request):
    context = {}
    if request.method == 'POST':
        form = LandingForm(request.POST)
        if form.is_valid():
            form.get_query()
            query_string = parse.urlencode({
                'type': form.type_choice,
                'interior': form.interior_choice
            })
            return HttpResponseRedirect(
                reverse('a:booking') + "?" + query_string
            )
        else:
            context['message'] = 'We could not process your request at this time'

    context['form'] = LandingForm()
    return render(request, 'index.html', context)


@login_required
def profile(request):
    context = {}
    return render(request, 'account/profile.html', context)


@login_required(login_url='/accounts/signup/')
def booking(request):
    context = {
        'initial_type_choice': request.GET.get('type'),
        'initial_interior_choice': request.GET.get('interior'),
    }

    if request.method == 'POST':
        form = BookingForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            query_string = parse.urlencode({
                'id': form.request_id
            })
            return HttpResponseRedirect(
                reverse('a:payment') + "?" + query_string
            )

        else:
            context['message'] = 'We could not process your request at this time'

    context['form'] = BookingForm(user=request.user)

    return render(request, 'booking.html', context)


@login_required
def payment(request):
    context = {

    }
    return render(request, 'payment.html', context)
