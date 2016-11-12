from django.conf.urls import url

from . import views


app_name = 'coconut'

urlpatterns = [
    url(r'^authenticate_user/', views.authenticate_user, name='authenticate_user'),
    url(r'^create_user/', views.create_user, name='create_user'),
]
