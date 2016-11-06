from django.conf.urls import url

from . import views


app_name = 'coconut'

urlpatterns = [
    url(r'^create_user/', views.create_user, name='create_user'),
]
