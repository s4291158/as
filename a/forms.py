from django import forms
from django.utils import timezone
from .models import BaseUser, Address, BankAccount, WashRequest, Car
from django.utils.translation import gettext as _


class LandingForm(forms.Form):
    type_choice = None
    interior_choice = None

    type_choices = [
        ('Hatchback', 25),
        ('Sedan', 29),
        ('Wagon', 35),
        ('SUV', 39),
        ('Van', 45),
    ]
    type_choices_dict = dict(type_choices)

    default_type_choice = type_choices[1][0]

    type_field = forms.CharField(
        initial=default_type_choice,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'hidden',
        })
    )

    interior_choices = [
        ('No Interior Cleaning', 0),
        ('Interior Vacuum & Wipe', 19),
    ]
    interior_choices_dict = dict(interior_choices)

    default_interior_choice = interior_choices[1][0]

    interior_field = forms.CharField(
        initial=default_interior_choice,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'hidden',
        })
    )

    def get_query(self):
        self.type_choice = self.cleaned_data['type_field']
        self.interior_choice = self.cleaned_data['interior_field']

    def save(self):
        self.get_query()
        save_request(self.type_choice, self.interior_choice)


class BookingForm(LandingForm):
    extra_dirty_choice = None

    extra_dirty_field = forms.BooleanField()

    def get_query(self):
        self.type_choice = self.cleaned_data['type_field']
        self.interior_choice = self.cleaned_data['interior_field']
        self.extra_dirty_choice = self.cleaned_data['extra_dirty_field']

    def save(self):
        save_request(self.type_choice, self.interior_choice, self.extra_dirty_choice)


def save_request(type_choice, interior_choice, extra_dirty_choice=False):
    car_price = LandingForm.types_dict.get(type_choice)
    interior_price = LandingForm.interiors_dict.get(interior_choice)
    dirty_price = (5 if extra_dirty_choice else 0)

    washrequest = WashRequest()

    washrequest.request_date = timezone.now()
    if interior_price == 0:
        washrequest.vacuum = False
        washrequest.wiping = False

    else:
        washrequest.vacuum = True
        washrequest.wiping = True
    washrequest.extra_dirty = extra_dirty_choice
    washrequest.total_price += sum([car_price, interior_price, dirty_price])
    washrequest.save()

    car = Car()
    car.washRequest = washrequest
    car.type = type_choice
    car.save()
