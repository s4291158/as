from django.conf.urls import url

from . import views


app_name = 'a'
urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^accounts/profile/', views.profile, name='profile'),

]
