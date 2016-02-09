from django import forms
from django.forms.forms import BoundField
from django.utils import timezone
from datetime import datetime
import collections

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

        for i in range(1, 6):
            self.fields['type_field' + str(i)] = forms.CharField()
            self.fields['interior_field' + str(i)] = forms.CharField()
            self.fields['car_specs_field' + str(i)] = forms.CharField()
            self.fields['extra_dirty_field' + str(i)] = forms.BooleanField()
            car_details = {
                'type_choice': None,
                'interior_choice': None,
                'extra_dirty_choice': None,
                'car_specs': None,
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
        self.booking['address'] = self.get_valid_address(street_address, suburb, state, postcode)

        self.booking['request']['wash_date'] = self.get_valid_wash_date(self.cleaned_data['wash_date_field'])

        self.booking['cars']['one']['type_choice'] = self.cleaned_data['type_field']
        self.booking['cars']['one']['interior_choice'] = self.cleaned_data['interior_field']
        self.booking['cars']['one']['extra_dirty_choice'] = self.cleaned_data['extra_dirty_field']
        self.booking['cars']['one']['car_specs'] = self.cleaned_data['car_specs_field']

    def save(self):
        self.get_cleaned_data()
        user = self.save_user()
        washee = self.save_washee(user)
        address = self.save_address(user)
        washrequest = self.save_wash_request(washee, address)
        car = self.save_car(washrequest)

    def save_user(self):
        user = BaseUser.objects.get(id=self.booking['user'].id)
        user.first_name = self.booking['personal']['first_name']
        user.last_name = self.booking['personal']['last_name']
        user.phone = self.booking['personal']['phone']
        user.role = "Washee"
        user.save()
        return user

    def save_washee(self, user):
        washee = Washee()
        washee.__dict__ = user.__dict__
        washee.save()
        return washee

    def save_address(self, user):
        if self.booking['address']:
            try:
                address = Address.objects.get(baseUser=user)
            except Address.DoesNotExist:
                address = Address()
                address.baseUser = user
            address.street_address = self.booking['address']['street_address']
            address.suburb = self.booking['address']['suburb']
            address.state = self.booking['address']['state']
            address.postcode = self.booking['address']['postcode']
            address.save()
            return address
        else:
            return None

    def save_wash_request(self, washee, address):
        car_price = LandingForm.type_choices_dict.get(self.booking['cars']['one']['type_choice'])
        interior_price = LandingForm.interior_choices_dict.get(self.booking['cars']['one']['interior_choice'])
        dirty_price = (5 if self.booking['cars']['one']['extra_dirty_choice'] else 0)

        washrequest = WashRequest()
        washrequest.washee = washee
        if self.booking['address']:
            washrequest.address = address
        washrequest.request_date = timezone.now()
        if self.booking['request']['wash_date']:
            washrequest.wash_date = self.booking['request']['wash_date']
        washrequest.total_price += sum([car_price, interior_price, dirty_price])
        washrequest.save()
        self.booking['request_id'] = washrequest.id
        return washrequest

    def save_car(self, washrequest):
        interior_price = LandingForm.interior_choices_dict.get(self.booking['cars']['one']['interior_choice'])

        car = Car()
        car.washRequest = washrequest
        if interior_price == 0:
            car.vacuum = False
            car.wiping = False
        else:
            car.vacuum = True
            car.wiping = True
        car.specs = self.booking['cars']['one']['car_specs']
        car.extra_dirty = self.booking['cars']['one']['extra_dirty_choice']
        car.type = self.booking['cars']['one']['type_choice']
        car.save()
        return car

    @staticmethod
    def get_valid_address(street_address, suburb, state, postcode):
        if not street_address and suburb and state and postcode:
            return None
        else:
            address = {
                'street_address': street_address,
                'suburb': suburb,
                'state': state,
                'postcode': postcode,
            }
            return address

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


class FieldSet(object):
    def __init__(self, form, fields, legend='', cls=None):
        self.form = form
        self.legend = legend
        self.fields = fields
        self.cls = cls

    def __iter__(self):
        for name in self.fields:
            field = self.form.fields[name]
            yield BoundField(self.form, field, name)
