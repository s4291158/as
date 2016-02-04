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
            print(query_string)
            print(parse.urlparse(reverse('a:booking') + "?" + query_string))
            # return HttpResponseRedirect(
            #     reverse('a:booking')
            # )
        else:
            context['message'] = 'We could not process your request at this time'

    context['form'] = LandingForm()
    return render(request, 'index.html', context)


@login_required
def profile(request):
    context = {}
    return render(request, 'account/profile.html', context)


@login_required(login_url='/accounts/signup/')
def booking(request, request_id=None):
    context = {
        'form': BookingForm(),
        'message': request_id,
    }

    return render(request, 'booking.html', context)
