from django.urls import path
from .views import input_controller, create_controller, set_public_key,reset_controller

urlpatterns = [
    path('input-controller/', input_controller, name='input_controller'),
    path('reset-controller/', reset_controller, name='reset_controller'),
    path('create-controller/', create_controller, name='create_controller'),
    path('setpbk/', set_public_key, name='set-public-key')
]
