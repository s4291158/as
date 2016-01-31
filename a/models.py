from django.db import models

from django.contrib.auth.models import AbstractUser


class BaseUser(AbstractUser):
    role = models.CharField(max_length=40, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)


class Washer(BaseUser):
    pass

    class Meta:
        verbose_name = 'Washer'


class Washee(BaseUser):
    pass

    class Meta:
        verbose_name = 'Washee'


class WashRequest(models.Model):
    washee = models.ForeignKey(Washee, on_delete=models.CASCADE)

    assigned_washer = models.ForeignKey(Washer, on_delete=models.CASCADE, blank=True)

    request_date = models.DateTimeField()
    wash_date = models.DateTimeField()
    water_details = models.CharField(max_length=40, blank=True)
    electricity_details = models.CharField(max_length=40, blank=True)
    vacuum_details = models.CharField(max_length=40, blank=True)
    description = models.CharField(max_length=254, blank=True)
    discount = models.FloatField(default=0, blank=True)
    total_price = models.FloatField(default=0, blank=True)


class Car(models.Model):
    washRequest = models.ForeignKey(WashRequest)

    number_plate = models.CharField(max_length=10, blank=True)
    type = models.CharField(max_length=10, blank=True)


class Address(models.Model):
    baseUser = models.OneToOneField(BaseUser, null=True)

    washRequest = models.OneToOneField(WashRequest, null=True)

    street_address = models.CharField(max_length=200)
    suburb = models.CharField(max_length=40)
    city = models.CharField(max_length=40, blank=True)
    postcode = models.IntegerField()
    state = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=40, blank=True)

    formatted = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.street_address


class BankAccount(models.Model):
    baseUser = models.OneToOneField(BaseUser)

    bank_name = models.CharField(max_length=40)
    bsb = models.IntegerField()
    account_number = models.IntegerField()
    account_holder = models.CharField(max_length=40)

    def __str__(self):
        return self.bank_name
