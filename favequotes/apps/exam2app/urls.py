from django.conf.urls import url
from . import views        
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^validate_login$', views.dash),
    url(r'^dash$', views.dash),
    url(r'^userquotes', views.userquotes),
    url(r'^editacct', views.editacct),
    url(r'^logout', views.logout)
]                
