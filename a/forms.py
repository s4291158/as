from django import forms
from django.utils import timezone
from .models import BaseUser, Address, BankAccount, WashRequest, Car
from django.utils.translation import gettext as _


class LandingForm(forms.Form):
    types = [
        ('Hatchback', 25),
        ('Sedan', 29),
        ('Wagon', 35),
        ('SUV', 39),
        ('Van', 45),
    ]
    types_dict = dict(types)

    default_type = types[1][0]

    type = forms.CharField(
        initial=default_type,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'hidden',
        })
    )

    interiors = [
        ('No Interior Cleaning', 0),
        ('Interior Vacuum & Wipe', 19),
    ]
    interiors_dict = dict(interiors)

    default_interior = interiors[1][0]

    interior = forms.CharField(
        initial=default_interior,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'hidden',
        })
    )

    def save(self):
        car_type = self.cleaned_data['type']
        interior_type = self.cleaned_data['interior']
        save_request(car_type, interior_type)


class BookingForm(LandingForm):
    extra_dirty = forms.BooleanField()

    def save(self):
        car_type = self.cleaned_data['type']
        interior_type = self.cleaned_data['interior']
        extra_dirty = self.cleand_data['extra_dirty']
        save_request(car_type, interior_type, extra_dirty)


def save_request(car_type, interior_type, extra_dirty=False):
    car_price = LandingForm.types_dict.get(car_type)
    interior_price = LandingForm.interiors_dict.get(interior_type)
    dirty_price = (5 if extra_dirty else 0)

    washrequest = WashRequest()
    washrequest.request_date = timezone.now()
    if interior_price == 0:
        washrequest.vacuum = False
        washrequest.wiping = False

    else:
        washrequest.vacuum = True
        washrequest.wiping = True
    washrequest.extra_dirty = extra_dirty
    washrequest.total_price += sum([car_price, interior_price, dirty_price])
    washrequest.save()

    car = Car()
    car.washRequest = washrequest
    car.type = car_type
    car.save()
