from django import forms
from django.utils import timezone
from datetime import datetime

from .models import BaseUser, Washee, Address, BankAccount, WashRequest, Car


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

    user = None

    first_name = None
    first_name_field = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'First Name',
        }))

    last_name = None
    last_name_field = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Last Name',
        }))

    phone = None
    phone_field = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Contact Number',
        }))

    email = None
    email_field = forms.EmailField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'email',
            'placeholder': 'Email Address   e.g. ',
            'readonly': True,
        }))

    street_address = None
    street_address_field = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Street Address  e.g. 24 raven street',
        }))

    suburb = None
    suburb_field = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Suburb  e.g. st lucia',
        }))

    state = None
    state_field = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'State   e.g. qld',
        }))

    postcode = None
    postcode_field = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Postcode    e.g. 4067',
        }))

    wash_date = None
    wash_date_field = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Wash date   e.g. 01/02/2016 5:20pm'
        }))

    car_specs = None
    car_specs_field = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Car make and model  e.g. Honda CRV'
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
        label='This car is really dirty, like seriously',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-control',
            'type': 'checkbox',
            'onclick': 'getTotalPrice();'
        }))

    def __init__(self, user, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['first_name_field'].initial = user.first_name
        self.fields['last_name_field'].initial = user.last_name
        self.fields['phone_field'].initial = user.phone
        self.fields['email_field'].initial = user.email

        try:
            address = Address.objects.get(baseUser=self.user)
            self.fields['street_address_field'].initial = address.street_address
            self.fields['suburb_field'].initial = address.suburb
            self.fields['state_field'].initial = address.state
            self.fields['postcode_field'].initial = address.postcode
        except Address.DoesNotExist:
            pass

    def get_cleaned_data(self):
        self.first_name = self.cleaned_data['first_name_field']
        self.last_name = self.cleaned_data['last_name_field']
        self.phone = self.cleaned_data['phone_field']

        self.street_address = self.cleaned_data['street_address_field']
        self.suburb = self.cleaned_data['suburb_field']
        self.state = self.cleaned_data['state_field']
        self.postcode = self.cleaned_data['postcode_field']

        self.wash_date = self.cleaned_data['wash_date_field']

        self.type_choice = self.cleaned_data['type_field']
        self.interior_choice = self.cleaned_data['interior_field']
        self.extra_dirty_choice = self.cleaned_data['extra_dirty_field']
        self.car_specs = self.cleaned_data['car_specs_field']

    def save(self):
        self.get_cleaned_data()

        car_price = LandingForm.type_choices_dict.get(self.type_choice)
        interior_price = LandingForm.interior_choices_dict.get(self.interior_choice)
        dirty_price = (5 if self.extra_dirty_choice else 0)

        user = BaseUser.objects.get(id=self.user.id)
        user.first_name = self.first_name
        user.last_name = self.last_name
        user.phone = self.phone
        user.role = "Washee"
        user.save()

        washee = Washee()
        washee.__dict__ = user.__dict__
        washee.save()

        if self.check_valid_address():
            try:
                address = Address.objects.get(baseUser=user)
            except Address.DoesNotExist:
                address = Address()
                address.baseUser = user
            address.street_address = self.street_address
            address.suburb = self.suburb
            address.state = self.state
            address.postcode = self.postcode
            address.save()

        washrequest = WashRequest()
        washrequest.washee = washee
        if self.check_valid_address():
            washrequest.address = address
        washrequest.request_date = timezone.now()
        wash_date = self.check_valid_wash_date()
        if wash_date:
            washrequest.wash_date = wash_date
        washrequest.total_price += sum([car_price, interior_price, dirty_price])
        washrequest.save()
        self.request_id = washrequest.id

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

    def check_valid_address(self):
        if not self.street_address and self.suburb and self.state and self.postcode:
            return False
        else:
            return True

    def check_valid_wash_date(self):
        if self.wash_date:
            try:
                wash_date = datetime.strptime(self.wash_date, "%d/%m/%Y %I:%M%p")
                wash_date = timezone.make_aware(wash_date, timezone.get_default_timezone())
                if wash_date > timezone.now():
                    return wash_date
            except ValueError:
                pass

        return None
