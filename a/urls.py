from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'a'
urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^booking/$', views.booking, name='booking'),
    url(r'^payment/$', views.payment, name='payment'),
    url(r'^washer/$', views.washer, name='washer'),

    url(r'^pricing/$', TemplateView.as_view(template_name='pricing.html'), name='pricing'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^insurance/$', TemplateView.as_view(template_name='insurance.html'), name='insurance'),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),

    url(r'^accounts/dashboard/$', views.dashboard, name='dashboard'),
    url(r'^accounts/profile/$', views.profile, name='profile'),

]
