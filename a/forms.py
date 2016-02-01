from django import forms
from django.utils import timezone
from .models import BaseUser, Address, BankAccount, WashRequest, Car


class LandingForm(forms.Form):
    class Meta:
        model = WashRequest

    oneline_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Car location e.g 123 abc st, brisbane CBD 4000',
        'class': 'form-control',
    }))

    types = [
        ('Small Sedan / Hatchback', 'Small Sedan / Hatchback'),
        ('Large Sedan / Wagon', 'Large Sedan / Wagon'),
        ('Small SUV', 'Small SUV'),
        ('Large SUV', 'Large SUV'),
        ('Van', 'Van')
    ]
    type = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Car Type e.g Sedan',
            'class': 'form-control',
        }))

    def save(self):
        washrequest = WashRequest()
        washrequest.request_date = timezone.now()
        washrequest.save()

        car = Car()
        car.washRequest = washrequest
        car.type = self.cleaned_data['type']
        car.save()
        washrequest.car_set.add(car)

        address = Address()
        address.washRequest = washrequest
        address.oneline_address = self.cleaned_data['oneline_address']
        address.save()
        washrequest.address = address

        washrequest.save()


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
