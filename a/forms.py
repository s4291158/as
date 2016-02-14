from django import forms
from django.forms.forms import BoundField
from django.utils import timezone
from datetime import datetime
import collections

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
        required=False,
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
        required=False,
        initial=default_interior_choice,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'hidden',
        })
    )

    car_fields = {
        'type_field': type_field,
        'interior_field': interior_field,
    }

    def get_query(self):
        self.type_choice = self.cleaned_data['type_field']
        self.interior_choice = self.cleaned_data['interior_field']


class BookingForm(LandingForm):
    booking = {
        'request_id': None,
        'user': None,
        'role': 'Washee',
        'personal': {
            'first_name': None,
            'last_name': None,
            'phone': None,
            'email': None,
        },
        'address': {
            'street_address': None,
            'suburb': None,
            'state': None,
            'postcode': None,
        },
        'request': {
            'wash_date': None,
            'car_count': None,
            'total_price': None,
        },
        'cars': collections.OrderedDict(),
    }

    def __init__(self, user, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.booking['user'] = user
        self.fields['first_name_field'] = forms.CharField(
            required=False,
            initial=user.first_name,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'First Name',
            }))
        self.fields['last_name_field'] = forms.CharField(
            required=False,
            initial=user.last_name,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Last Name',
            }))
        self.fields['phone_field'] = forms.CharField(
            required=False,
            initial=user.phone,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Contact Number',
            }))
        self.fields['email_field'] = forms.EmailField(
            required=False,
            initial=user.email,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'email',
                'placeholder': 'Email Address',
                'readonly': True,
            }))

        self.fields['street_address_field'] = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Street Address',
            }))

        self.fields['suburb_field'] = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Suburb',
            }))

        self.fields['state_field'] = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'State',
            }))

        self.fields['postcode_field'] = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Postcode',
            }))

        try:
            address = Address.objects.get(baseUser=self.booking['user'])
            self.fields['street_address_field'].initial = address.street_address
            self.fields['suburb_field'].initial = address.suburb
            self.fields['state_field'].initial = address.state
            self.fields['postcode_field'].initial = address.postcode
        except Address.DoesNotExist:
            pass

        self.fields['wash_date_field'] = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Wash date   e.g. 01/02/2016 5:20pm'
            }))

        self.fields['car_count_field'] = forms.IntegerField(
            initial=1,
            required=False,
            widget=forms.TextInput(attrs={
                'type': 'hidden',
            })
        )

        for i in range(1, 6):
            self.fields['type_field' + str(i)] = forms.CharField(required=False)
            self.fields['interior_field' + str(i)] = forms.CharField(required=False)
            self.fields['car_specs_field' + str(i)] = forms.CharField(required=False)
            self.fields['extra_dirty_field' + str(i)] = forms.BooleanField(required=False)
            car_details = {
                'type_choice': None,
                'interior_choice': None,
                'extra_dirty_choice': None,
                'car_specs': None,
                'price': None,
            }
            self.booking['cars'][str(i)] = car_details

    def get_cleaned_data(self):
        self.booking['personal']['first_name'] = self.cleaned_data['first_name_field']
        self.booking['personal']['last_name'] = self.cleaned_data['last_name_field']
        self.booking['personal']['phone'] = self.cleaned_data['phone_field']

        street_address = self.cleaned_data['street_address_field']
        suburb = self.cleaned_data['suburb_field']
        state = self.cleaned_data['state_field']
        postcode = self.cleaned_data['postcode_field']
        self.booking['address'] = get_valid_address(street_address, suburb, state, postcode)

        self.booking['request']['wash_date'] = self.get_valid_wash_date(self.cleaned_data['wash_date_field'])
        self.booking['request']['car_count'] = self.cleaned_data['car_count_field']

        for i in range(1, self.booking['request']['car_count'] + 1):
            self.booking['cars'][str(i)]['type_choice'] = self.cleaned_data['type_field' + str(i)]
            self.booking['cars'][str(i)]['interior_choice'] = self.cleaned_data['interior_field' + str(i)]
            self.booking['cars'][str(i)]['extra_dirty_choice'] = self.cleaned_data['extra_dirty_field' + str(i)]
            self.booking['cars'][str(i)]['car_specs'] = self.cleaned_data['car_specs_field' + str(i)]
            self.booking['cars'][str(i)]['price'] = self.get_car_price(i)

    def save(self):
        self.get_cleaned_data()
        user = save_user(self.booking)
        address = save_address(self.booking, user)
        washrequest = self.save_wash_request(user, address)
        self.save_car(washrequest)

    def save_wash_request(self, user, address):
        washrequest = WashRequest()
        washrequest.washee = user
        if self.booking['address']:
            washrequest.address = address
        washrequest.request_date = timezone.now()
        if self.booking['request']['wash_date']:
            washrequest.wash_date = self.booking['request']['wash_date']
        washrequest.car_count = self.booking['request']['car_count']
        washrequest.total_price = self.get_total_price()
        washrequest.save()
        self.booking['request_id'] = washrequest.id
        return washrequest

    def save_car(self, washrequest):
        for i in range(1, self.booking['request']['car_count'] + 1):
            car = Car()
            car.washRequest = washrequest

            interior_price = LandingForm.interior_choices_dict.get(self.booking['cars'][str(i)]['interior_choice'])
            if interior_price == 0:
                car.vacuum = False
                car.wiping = False
            else:
                car.vacuum = True
                car.wiping = True

            specs = self.booking['cars'][str(i)]['car_specs']
            if specs:
                car.specs = specs
            else:
                car.specs = 'Car' + str(i)
            car.extra_dirty = self.booking['cars'][str(i)]['extra_dirty_choice']
            car.type = self.booking['cars'][str(i)]['type_choice']
            car.price = self.get_car_price(i)
            car.save()

    @staticmethod
    def get_valid_wash_date(wash_date):
        if wash_date:
            try:
                wash_date_cleaned = datetime.strptime(wash_date, "%d/%m/%Y %I:%M%p")
                wash_date_cleaned = timezone.make_aware(wash_date_cleaned, timezone.get_default_timezone())
                if wash_date_cleaned > timezone.now():
                    return wash_date_cleaned
            except ValueError:
                pass

        return None

    def get_car_price(self, i):
        car_price = LandingForm.type_choices_dict.get(self.booking['cars'][str(i)]['type_choice'])
        interior_price = LandingForm.interior_choices_dict.get(self.booking['cars'][str(i)]['interior_choice'])
        dirty_price = (5 if self.booking['cars'][str(i)]['extra_dirty_choice'] else 0)
        car_price = sum([car_price, interior_price, dirty_price])
        return car_price

    def get_total_price(self):
        total_price = 0
        for i in range(1, self.booking['request']['car_count'] + 1):
            total_price += self.get_car_price(i)
        return total_price


class WasherForm(forms.Form):
    washer = {
        'user': None,
        'role': 'Washer',
        'personal': {
            'first_name': None,
            'last_name': None,
            'phone': None,
            'email': None,
        },
    }

    def __init__(self, user, *args, **kwargs):
        super(WasherForm, self).__init__(*args, **kwargs)
        self.washer['user'] = user

        self.fields['first_name_field'] = forms.CharField(
            required=False,
            initial=user.first_name,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'First Name',
            }))
        self.fields['last_name_field'] = forms.CharField(
            required=False,
            initial=user.last_name,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Last Name',
            }))
        self.fields['phone_field'] = forms.CharField(
            required=False,
            initial=user.phone,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Contact Number',
            }))
        self.fields['email_field'] = forms.EmailField(
            required=False,
            initial=user.email,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'email',
                'placeholder': 'Email Address',
                'readonly': True,
            }))

    def get_cleaned_data(self):
        self.washer['personal']['first_name'] = self.cleaned_data['first_name_field']
        self.washer['personal']['last_name'] = self.cleaned_data['last_name_field']
        self.washer['personal']['phone'] = self.cleaned_data['phone_field']

    def save(self):
        self.get_cleaned_data()
        user = save_user(self.washer)


def save_user(data):
    user = BaseUser.objects.get(id=data['user'].id)
    user.first_name = data['personal']['first_name']
    user.last_name = data['personal']['last_name']
    user.phone = data['personal']['phone']
    user.role = data['role']
    user.save()
    return user


def save_address(data, user):
    if data['address']:
        try:
            address = Address.objects.get(baseUser=user)
        except Address.DoesNotExist:
            address = Address()
            address.baseUser = user
        address.street_address = data['address']['street_address']
        address.suburb = data['address']['suburb']
        address.state = data['address']['state']
        address.postcode = data['address']['postcode']
        address.oneline_address = data['address']['oneline_address']
        address.save()
        return address
    else:
        return None


def get_valid_address(street_address, suburb, state, postcode):
    if not street_address and suburb and state and postcode:
        return None
    else:
        oneline_address = ''
        if street_address:
            oneline_address += street_address + ','
        if suburb:
            oneline_address += ' ' + suburb
        if state:
            oneline_address += ' ' + state
        if postcode:
            oneline_address += ' ' + postcode
        address = {
            'street_address': street_address,
            'suburb': suburb,
            'state': state,
            'postcode': postcode,
            'oneline_address': oneline_address,
        }
        return address
