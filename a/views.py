from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden

from allauth.account.views import SignupView

from .forms import LandingForm, BookingForm, WasherForm
from .models import WashRequest, BaseUser

from urllib import parse


def index(request):
    context = {}
    if request.method == 'POST':
        form = LandingForm(request.POST)
        if form.is_valid():
            form.get_cleaned_data()
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
def washer(request):
    context = {}

    if request.method == 'POST':
        form = WasherForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('a:profile'))

        else:
            context['message'] = 'We could not process your request at this time'
            context['form'] = form

    else:
        context['form'] = WasherForm(user=request.user)

    return render(request, 'washer.html', context)


@login_required(login_url='/accounts/signup/')
def booking(request):
    context = {
        'initial_type_choice': request.GET['type'],
        'initial_interior_choice': request.GET['interior'],
    }

    if request.method == 'POST':
        form = BookingForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            query_string = parse.urlencode({
                'id': form.booking['request_id']
            })
            return HttpResponseRedirect(
                reverse('a:payment') + "?" + query_string
            )

        else:
            context['message'] = 'We could not process your request at this time'
            context['form'] = form

    else:
        context['form'] = BookingForm(user=request.user)

    return render(request, 'booking.html', context)


@login_required
def payment(request):
    washrequest = WashRequest.objects.get(id=request.GET['id'])
    if request.user.id == washrequest.washee.id or request.user.is_superuser:
        context = {
            'wash_request': washrequest,
        }
        return render(request, 'payment.html', context)

    else:
        return HttpResponseForbidden()
