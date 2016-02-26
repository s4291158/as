from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound, \
    Http404, \
    JsonResponse

from .forms import *
from .models import WashRequest, BaseUser

from urllib import parse


def admin_change_role(request):
    context = {}
    if request.method == 'POST':
        form = AdminChangeRoleForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            context['role'] = form.cleaned_data['role_field']
    # return JsonResponse(context)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def index(request):
    context = {}
    if request.method == 'POST':
        form = LandingForm(request.POST)
        if form.is_valid():
            query_string = parse.urlencode({
                'type': form.cleaned_data['type_field'],
                'interior': form.cleaned_data['interior_field'],
            })
            return HttpResponseRedirect(
                reverse('a:booking') + "?" + query_string
            )
        else:
            context['message'] = 'We could not process your request at this time'

    context['form'] = LandingForm()
    return render(request, 'index.html', context)


@login_required
def dashboard(request):
    context = {}

    if request.user.role == 'user':
        context['message'] = 'Book a request now or sign up to become an AirSponge washer'
    elif request.user.role == 'washee':
        context['active_requests'] = WashRequest.objects.filter(washee=request.user, active=True).order_by(
            'request_date').reverse()
        context['inactive_requests'] = WashRequest.objects.filter(washee=request.user, active=False).order_by(
            'request_date').reverse()
    elif request.user.role == 'washer':
        context['available_requests'] = WashRequest.objects.filter(status='confirmed').order_by(
            'request_date').reverse()
        context['active_requests'] = WashRequest.objects.filter(washer=request.user, active=True).order_by(
            'request_date').reverse()
        context['inactive_requests'] = WashRequest.objects.filter(washer=request.user, active=False).order_by(
            'request_date').reverse()
    return render(request, 'account/dashboard.html', context)


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
            context['message'] = 'We could not process your request at this time, please check field errors'
            context['form'] = form

    else:
        if request.user.role == 'washee' or request.user.role == 'both':
            context['form'] = LandingForm()
            context['message'] = 'We require separate accounts to provide and use our service'
            return render(request, 'index.html', context)
        else:
            context['form'] = WasherForm(user=request.user)

    return render(request, 'washer.html', context)


@login_required(login_url='/accounts/signup/')
def booking(request):
    context = {}
    request_id = None
    if 'type' in request.GET:
        context['initial_type_choice'] = request.GET['type']
    if 'interior' in request.GET:
        context['initial_interior_choice'] = request.GET['interior']
    if 'id' in request.GET:
        request_id = request.GET['id']

    if request.user.role == 'washer' or request.user.role == 'both':
        context['form'] = LandingForm()
        context['message'] = 'We require separate accounts to provide and use our service'
        return render(request, 'index.html', context)

    if request.method == 'POST':
        form = BookingForm(request.user, request.POST)
        if form.is_valid():
            form.booking['request_id'] = request_id
            form.save()
            query_string = parse.urlencode({
                'id': form.booking['request_id']
            })
            return HttpResponseRedirect(
                reverse('a:carwash') + "?" + query_string
            )

        else:
            context['message'] = 'We could not process your request at this time, please check field errors'
            context['form'] = form
    elif request_id:
        try:
            washrequest = WashRequest.objects.get(id=request_id)
        except WashRequest.DoesNotExist:
            return HttpResponseNotFound()
        if can_see_carwash(request.user, washrequest.washee):
            initial_value = {
                'wash_date_field': washrequest.wash_date,
                'car_count_field': washrequest.car_count,
            }
            if washrequest.promocode:
                initial_value['promocode_field'] = washrequest.promocode.code
            for i, car in enumerate(washrequest.car_set.iterator()):
                i = str(i + 1)
                initial_value['car_specs_field' + i] = car.specs
                initial_value['type_field' + i] = car.type
                if car.vacuum and car.wiping:
                    initial_value['interior_field' + i] = 'both'
                elif not car.vacuum and not car.wiping:
                    initial_value['interior_field' + i] = 'none'
                initial_value['extra_dirty_field' + i] = car.extra_dirty

            context['form'] = BookingForm(user=request.user, initial=initial_value)
        else:
            return HttpResponseForbidden()
    else:
        context['form'] = BookingForm(user=request.user)

    return render(request, 'booking.html', context)


@login_required
def carwash(request):
    if 'id' in request.GET:
        try:
            washrequest = WashRequest.objects.get(id=request.GET['id'])
        except WashRequest.DoesNotExist:
            raise Http404

        if can_see_carwash(request.user, washrequest.washee):
            if 'action' in request.GET and request.user.role == 'washee':
                action = request.GET['action']
                if action == 'cancel':
                    washrequest.status = 'cancelled'
                    washrequest.active = False
                    washrequest.save()
                else:
                    return HttpResponseBadRequest()

            context = {
                'wash_request': washrequest,
            }

            return render(request, 'carwash.html', context)
        else:
            return HttpResponseForbidden()


    else:
        return HttpResponseBadRequest()


def can_see_carwash(user, washee):
    if user.id == washee.id or user.role == 'washer' or user.role == 'both':
        return True
    else:
        return False
