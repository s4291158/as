from django import forms
from django.utils import timezone
from datetime import datetime
import collections
import random

from .models import *


class LandingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LandingForm, self).__init__(*args, **kwargs)
        self.fields['type_field'] = forms.CharField(
            required=False,
            initial='Sedan',
            widget=forms.Select(
                attrs={
                    'class': 'form-control no-border-radius',
                    'onchange': 'getTotalPrice();',
                }, choices=(
                    ('Hatchback', '$25 — Hatchback'),
                    ('Sedan', '$29 — Sedan'),
                    ('Wagon', '$35 — Wagon'),
                    ('SUV', '$39 — SUV'),
                    ('Van', '$45 — Van'),
                )
            )
        )
        self.fields['interior_field'] = forms.CharField(
            required=False,
            initial='both',
            widget=forms.Select(
                attrs={
                    'class': 'form-control no-border-radius',
                    'onchange': 'getTotalPrice();',
                }, choices=(
                    ('none', '$0 — No interior cleaning'),
                    ('both', '$19 — Interior vacuum & wipe'),
                )
            )
        )


class BaseUserForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(BaseUserForm, self).__init__(*args, **kwargs)

        self.fields['first_name_field'] = forms.CharField(
            initial=user.first_name,
            label='First name',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
            }))
        self.fields['last_name_field'] = forms.CharField(
            initial=user.last_name,
            label='Last name',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
            }))
        self.fields['phone_field'] = forms.CharField(
            initial=user.phone,
            label='Phone number',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact Number',
            }))
        self.fields['email_field'] = forms.EmailField(
            initial=user.email,
            label='Email address',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'email',
                'placeholder': 'Email Address',
                'readonly': True,
            }))

        self.fields['street_address_field'] = forms.CharField(
            label='Street address',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street Address',
            }))
        self.fields['suburb_field'] = forms.CharField(
            label='Suburb',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Suburb',
            }))
        self.fields['state_field'] = forms.CharField(
            required=False,
            label='State',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State',
            }))
        self.fields['postcode_field'] = forms.CharField(
            required=False,
            label='Postcode',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postcode',
            }))

        try:
            address = Address.objects.get(baseUser=user)
            self.fields['street_address_field'].initial = address.street_address
            self.fields['suburb_field'].initial = address.suburb
            self.fields['state_field'].initial = address.state
            self.fields['postcode_field'].initial = address.postcode
        except Address.DoesNotExist:
            pass


class WasherForm(BaseUserForm):
    washer = {
        'user': None,
        'role': 'washer',
        'personal': {},
        'address': {},
        'questions': {},
    }

    def __init__(self, user, *args, **kwargs):
        super(WasherForm, self).__init__(user, *args, **kwargs)
        self.washer['user'] = user

        self.fields['has_car_field'] = forms.BooleanField(
            required=False,
            label='Do you have a car?',
        )
        self.fields['has_hose_field'] = forms.BooleanField(
            required=False,
            label='Can you bring a hose?',
        )
        self.fields['vacuum_type_field'] = forms.CharField(
            required=False,
            label='What type of vacuum cleaner do you have?',
        )
        self.fields['travel_distance_field'] = forms.IntegerField(
            label="What is the max distance(km) you're willing to travel?",
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Typically each km is 2mins of driving',
            })
        )
        self.fields['availability_field'] = forms.CharField(
            label='Tell us about your availability through out the week',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '9am-5pm weekdays, all day weekends',
            })
        )
        self.fields['experience_field'] = forms.CharField(

            label='Finally, write a little about your carwashing experience',
            widget=forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '10',
                'placeholder': "I wash my own car when I run out of things to do... It counts right?",
            })
        )

    def get_cleaned_data(self):
        self.washer['personal'] = cleaned_personal(self.cleaned_data)
        self.washer['address'] = cleaned_address(self.cleaned_data)

        self.washer['questions']['has_car'] = self.cleaned_data['has_car_field']
        self.washer['questions']['has_hose'] = self.cleaned_data['has_hose_field']
        self.washer['questions']['vacuum_type'] = self.cleaned_data['vacuum_type_field']
        try:
            self.washer['questions']['travel_distance'] = int(self.cleaned_data['travel_distance_field'])
        except ValueError:
            self.washer['questions']['travel_distance'] = 0
        self.washer['questions']['availability'] = self.cleaned_data['availability_field']
        self.washer['questions']['experience'] = self.cleaned_data['experience_field']

    def save(self):
        self.get_cleaned_data()
        user = save_user(self.washer)
        address = save_address(self.washer, user)
        washer = self.save_washer(user)

    def save_washer(self, user):
        try:
            washer = Washer.objects.get(baseUser=user)
        except Washer.DoesNotExist:
            washer = Washer()
            washer.baseUser = user
        washer.has_car = self.washer['questions']['has_car']
        washer.has_hose = self.washer['questions']['has_hose']
        washer.vacuum_type = self.washer['questions']['vacuum_type']
        washer.travel_distance = self.washer['questions']['travel_distance']
        washer.availability = self.washer['questions']['availability']
        washer.experience = self.washer['questions']['experience']
        washer.save()
        return washer


class BookingForm(BaseUserForm):
    type_price_dict = {
        'Hatchback': 25,
        'Sedan': 29,
        'Wagon': 35,
        'SUV': 39,
        'Van': 45
    }
    interior_price_dict = {
        'none': 0,
        'both': 19
    }
    extra_dirty_texts = [
        "The car is really dirty... like seriously",
        "It is unbelivable how dirty this car is, like you wouldn't believe",
        "Took it for a spin in a shit storm and now the car is full of shit... literally",
        "Car is extra dirty",
    ]
    booking = {
        'request_id': None,
        'user': None,
        'role': 'washee',
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
            'oneline_address': None,
        },
        'request': {
            'wash_date': None,
            'car_count': None,
            'total_price': None,
        },
        'cars': collections.OrderedDict(),
    }

    def __init__(self, user, *args, **kwargs):
        super(BookingForm, self).__init__(user, *args, **kwargs)
        self.booking['user'] = user

        self.fields['wash_date_field'] = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Wash date   e.g. 01/02/2016 5:20pm'
            })
        )
        self.fields['promocode_field'] = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Promocode'
            })
        )
        self.fields['car_count_field'] = forms.IntegerField(
            initial=1,
            required=False,
            widget=forms.TextInput(attrs={
                'type': 'hidden',
            })
        )
        for i in range(1, 6):
            self.fields['car_specs_field' + str(i)] = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Car make and model'
                })
            )
            self.fields['type_field' + str(i)] = forms.CharField(
                required=False,
                initial='Sedan',
                widget=forms.Select(
                    attrs={
                        'class': 'form-control',
                        'onchange': 'getTotalPrice();',
                    }, choices=(
                        ('Hatchback', '$25 — Hatchback'),
                        ('Sedan', '$29 — Sedan'),
                        ('Wagon', '$35 — Wagon'),
                        ('SUV', '$39 — SUV'),
                        ('Van', '$45 — Van'),
                    )
                )
            )
            self.fields['interior_field' + str(i)] = forms.CharField(
                required=False,
                initial='both',
                widget=forms.Select(
                    attrs={
                        'class': 'form-control',
                        'onchange': 'getTotalPrice();',
                    }, choices=(
                        ('none', '$0 — No interior cleaning'),
                        ('both', '$19 — Interior vacuum & wipe'),
                    )
                )
            )
            self.fields['extra_dirty_field' + str(i)] = forms.BooleanField(
                required=False,
                label=random.choice(self.extra_dirty_texts),
                widget=forms.CheckboxInput(attrs={
                    'class': 'form-control',
                    'onclick': 'getTotalPrice();',
                })
            )

            car_details = {
                'type_choice': None,
                'interior_choice': None,
                'extra_dirty_choice': None,
                'car_specs': None,
                'price': None,
            }
            self.booking['cars'][str(i)] = car_details

    def get_cleaned_data(self):
        self.booking['personal'] = cleaned_personal(self.cleaned_data)
        self.booking['address'] = cleaned_address(self.cleaned_data)

        self.booking['request']['wash_date'] = self.get_valid_wash_date(self.cleaned_data['wash_date_field'])
        self.booking['request']['promocode'] = self.cleaned_data['promocode_field']
        self.booking['request']['car_count'] = self.cleaned_data['car_count_field']

        for i in range(1, self.booking['request']['car_count'] + 1):
            self.booking['cars'][str(i)]['type_choice'] = self.cleaned_data['type_field' + str(i)]
            self.booking['cars'][str(i)]['interior_choice'] = self.cleaned_data['interior_field' + str(i)]
            self.booking['cars'][str(i)]['extra_dirty_choice'] = self.cleaned_data['extra_dirty_field' + str(i)]
            self.booking['cars'][str(i)]['car_specs'] = self.cleaned_data['car_specs_field' + str(i)]
            self.booking['cars'][str(i)]['price'] = self.get_car_price(i)

    def clean_promocode_field(self):
        if self.cleaned_data['promocode_field']:
            try:
                promocode = Promocode.objects.get(code=self.cleaned_data['promocode_field'])
                if promocode.end_date and timezone.now().date() > promocode.end_date:
                    raise forms.ValidationError('Promocode has expired')
                else:
                    if promocode.max_usage and promocode.usage >= promocode.max_usage:
                        raise forms.ValidationError('Promocode has been used')
            except Promocode.DoesNotExist:
                raise forms.ValidationError('Promocode does not exist')
        return self.cleaned_data['promocode_field']

    def save(self):
        self.get_cleaned_data()
        user = save_user(self.booking)
        address = save_address(self.booking, user)
        washrequest = self.save_wash_request(user, address)
        self.save_car(washrequest)
        self.booking['request_id'] = washrequest.id

    def save_wash_request(self, user, address):
        if self.booking['request_id']:
            washrequest = WashRequest.objects.get(id=self.booking['request_id'])
        else:
            washrequest = WashRequest()

        washrequest.washee = user

        if address:
            washrequest.address = address

        washrequest.request_date = timezone.now()
        if self.booking['request']['wash_date']:
            washrequest.wash_date = self.booking['request']['wash_date']

        washrequest.car_count = self.booking['request']['car_count']

        washrequest.total_price = self.get_total_price()

        if self.booking['request']['promocode']:
            washrequest.promocode = Promocode.objects.get(code=self.booking['request']['promocode'])
            if washrequest.promocode.discount_type == '$':
                washrequest.discount = washrequest.promocode.discount
                washrequest.total_price -= washrequest.discount
            elif washrequest.promocode.discount_type == '%':
                washrequest.discount = washrequest.total_price * (1 - washrequest.promocode / 100)
                washrequest.total_price -= washrequest.discount

        washrequest.save()

        return washrequest

    def save_car(self, washrequest):
        if self.booking['request_id']:
            carset = Car.objects.filter(washRequest=washrequest)
        else:
            carset = None
        for i in range(1, self.booking['request']['car_count'] + 1):

            if carset and i <= len(carset):
                car = carset[i - 1]
            else:
                car = Car()
            car.washRequest = washrequest

            if self.booking['cars'][str(i)]['interior_choice'] == 'none':
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
        car_price = self.type_price_dict[self.booking['cars'][str(i)]['type_choice']]
        interior_price = self.interior_price_dict[self.booking['cars'][str(i)]['interior_choice']]
        dirty_price = (5 if self.booking['cars'][str(i)]['extra_dirty_choice'] else 0)
        car_price = sum([car_price, interior_price, dirty_price])
        return car_price

    def get_total_price(self):
        total_price = 0
        for i in range(1, self.booking['request']['car_count'] + 1):
            total_price += self.get_car_price(i)
        return total_price


##############################
# OUTSIDE-OF-CLASS FUNCTIONS #
##############################

def cleaned_personal(cleaned_data):
    personal = {
        'first_name': cleaned_data['first_name_field'],
        'last_name': cleaned_data['last_name_field'],
        'phone': cleaned_data['phone_field']
    }
    return personal


def cleaned_address(cleaned_data):
    street_address = cleaned_data['street_address_field']
    suburb = cleaned_data['suburb_field']
    state = cleaned_data['state_field']
    postcode = cleaned_data['postcode_field']
    address = get_valid_address(street_address, suburb, state, postcode)
    return address


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
