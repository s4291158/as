from django import forms
from django.utils import timezone
from .models import BaseUser, Address, BankAccount, WashRequest, Car


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
        car_price = self.types_dict.get(car_type)
        interior_type = self.cleaned_data['interior']
        interior_price = self.interiors_dict.get(interior_type)

        washrequest = WashRequest()
        washrequest.request_date = timezone.now()
        if interior_price == 0:
            washrequest.vacuum = False
            washrequest.wiping = False

        else:
            washrequest.vacuum = True
            washrequest.wiping = True
        washrequest.total_price += car_price
        washrequest.total_price += interior_price
        washrequest.save()

        car = Car()
        car.washRequest = washrequest
        car.type = car_type
        car.save()

    def strip_type(self, field):
        return self.cleaned_data[field].replace("$", "").split(' - ')[1]


class CustomSignupForm(forms.Form):
    class Meta:
        model = BaseUser

        fieldsets = (
            ('Account', {'fields': ['email', 'password1', 'password2']}),
            ('Personal', {'fields': ['first_name', 'last_name', 'phone']}),
            ('Address', {'fields': ['street_address', 'suburb', 'postcode']}),
            ('Bank', {'fields': ['bank_name', 'bsb', 'account_number', 'account_holder']}),
        )

    email = forms.EmailField()
    password1 = forms.CharField()

    # first_name = forms.CharField()
    # last_name = forms.CharField()
    # phone = forms.IntegerField()
    #
    # street_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '123 abc street'}))
    # suburb = forms.CharField()
    # postcode = forms.IntegerField()

    # bank_name = forms.CharField()
    # bsb = forms.IntegerField()
    # account_number = forms.IntegerField()
    # account_holder = forms.CharField()

    def save(self, user):
        # user.phone = self.cleaned_data['phone']
        #
        # address = Address()
        # address.baseUser = user
        # address.street_address = self.cleaned_data['street_address']
        # address.suburb = self.cleaned_data['suburb']
        # address.postcode = self.cleaned_data['postcode']
        # address.save()
        #
        # user.address = address
        user.save()
