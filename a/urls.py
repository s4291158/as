from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


app_name = 'a'
urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^pricing/', TemplateView.as_view(template_name='pricing.html')),
    url(r'^about/', TemplateView.as_view(template_name='about.html')),
    url(r'^insurance/', TemplateView.as_view(template_name='insurance.html')),
    url(r'^contact/', TemplateView.as_view(template_name='contact.html')),
    url(r'^accounts/profile/', views.profile, name='profile'),

]
