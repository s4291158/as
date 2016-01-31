from django import forms
from .models import BaseUser, Address, BankAccount


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
    password2 = forms.CharField()

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.IntegerField()

    street_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '123 abc street'}))
    suburb = forms.CharField()
    postcode = forms.IntegerField()

    # bank_name = forms.CharField()
    # bsb = forms.IntegerField()
    # account_number = forms.IntegerField()
    # account_holder = forms.CharField()

    def save(self, user):
        user.phone = self.cleaned_data['phone']

        address = Address()
        address.baseUser = user
        address.street_address = self.cleaned_data['street_address']
        address.suburb = self.cleaned_data['suburb']
        address.postcode = self.cleaned_data['postcode']
        address.save()

        user.address = address
        user.save()
