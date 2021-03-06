from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def get_car_specs_field(form, i):
    return form['car_specs_field' + str(i)]


@register.filter
def get_type_field(form, i=''):
    return form['type_field' + str(i)]


@register.filter
def get_interior_field(form, i=''):
    return form['interior_field' + str(i)]


@register.filter
def get_extra_dirty_field(form, i):
    return form['extra_dirty_field' + str(i)]


@register.filter
def get_extra_dirty_field_label(form, i):
    return form['extra_dirty_field' + str(i)].label


@register.filter(name='url_address')
def url_address(address):
    return address.replace(' ', '+')
