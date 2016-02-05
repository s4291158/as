from django.db import models

from django.contrib.auth.models import AbstractUser


class BaseUser(AbstractUser):
    role = models.CharField(max_length=40, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
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
    washee = models.ForeignKey(Washee, on_delete=models.CASCADE, null=True, blank=True)

    assigned_washer = models.ForeignKey(Washer, on_delete=models.CASCADE, null=True, blank=True)

    confirmed = models.BooleanField(default=False)

    request_date = models.DateTimeField(null=True, blank=True)
    wash_date = models.DateTimeField(null=True, blank=True)
    water_details = models.CharField(max_length=40, null=True, blank=True)
    electricity_details = models.CharField(max_length=40, null=True, blank=True)
    vacuum_details = models.CharField(max_length=40, null=True, blank=True)
    description = models.CharField(max_length=254, null=True, blank=True)
    discount = models.FloatField(default=0, blank=True)
    total_price = models.FloatField(default=0, blank=True)

    def __str__(self):
        return 'wash no.' + str(self.id)


class Car(models.Model):
    washRequest = models.ForeignKey(WashRequest, null=True)

    specs = models.CharField(max_length=40, null=True, blank=True)
    number_plate = models.CharField(max_length=10, null=True, blank=True)
    type = models.CharField(max_length=40, null=True, blank=True)
    dirtiness = models.IntegerField(null=True, blank=True)
    extra_dirty = models.BooleanField(default=False)
    vacuum = models.BooleanField(default=True)
    wiping = models.BooleanField(default=True)

    def __str__(self):
        return self.type


class Address(models.Model):
    baseUser = models.OneToOneField(BaseUser, null=True, blank=True)

    washRequest = models.OneToOneField(WashRequest, null=True, blank=True)

    street_address = models.CharField(max_length=200, null=True, blank=True)
    suburb = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=40, null=True, blank=True)
    postcode = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=40, null=True, blank=True)

    oneline_address = models.CharField(max_length=200, null=True, blank=True)
    formatted = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.oneline_address:
            return self.oneline_address
        else:
            return self.street_address + ', ' + self.suburb + str(self.postcode)


class BankAccount(models.Model):
    baseUser = models.OneToOneField(BaseUser)

    bank_name = models.CharField(max_length=40, null=True, blank=True)
    bsb = models.IntegerField(null=True, blank=True)
    account_number = models.IntegerField(null=True, blank=True)
    account_holder = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return self.bank_name
