from django import forms
from django.utils import timezone

from .models import BaseUser, Address, BankAccount, WashRequest, Car


class LandingForm(forms.Form):
    type_choice = None
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

    interior_choice = None
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


class BookingForm(LandingForm):
    request_id = None

    first_name = None
    first_name_field = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'placeholder': 'First Name',
    }))

    last_name = None
    last_name_field = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'placeholder': 'Last Name',
    }))

    phone = None
    phone_field = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'placeholder': 'Contact Number',
    }))

    email = None
    email_field = forms.EmailField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'email',
        'placeholder': 'Email Address',
    }))

    car_specs = None
    car_specs_field = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'placeholder': 'Car make, model, color and/or number plate'
    }))

    extra_dirty_choice = None
    extra_dirty_choices = [
        ('No', 0),
        ('Yes', 5),
    ]
    extra_dirty_choices_dict = dict(extra_dirty_choices)
    default_extra_dirty_choice = extra_dirty_choices[0][0]
    extra_dirty_field = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'hidden',
        }))

    wash_date_field = forms.CharField(
        initial=timezone.now(),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }))

    def get_cleaned_data(self):
        self.first_name = self.cleaned_data['first_name_field']
        self.last_name = self.cleaned_data['last_name_field']
        self.phone = self.cleaned_data['phone_field']
        self.email = self.cleaned_data['email_field']

        self.type_choice = self.cleaned_data['type_field']
        self.interior_choice = self.cleaned_data['interior_field']
        self.extra_dirty_choice = self.cleaned_data['extra_dirty_field']
        self.car_specs = self.cleaned_data['car_specs_field']

    def save(self):
        self.get_cleaned_data()

        car_price = LandingForm.type_choices_dict.get(self.type_choice)
        interior_price = LandingForm.interior_choices_dict.get(self.interior_choice)
        dirty_price = (5 if self.extra_dirty_choice else 0)

        washrequest = WashRequest()
        self.request_id = washrequest.id
        washrequest.request_date = timezone.now()
        washrequest.total_price += sum([car_price, interior_price, dirty_price])
        washrequest.save()

        car = Car()
        car.washRequest = washrequest
        if interior_price == 0:
            car.vacuum = False
            car.wiping = False
        else:
            car.vacuum = True
            car.wiping = True
        car.specs = self.car_specs
        car.extra_dirty = self.extra_dirty_choice
        car.type = self.type_choice
        car.save()
