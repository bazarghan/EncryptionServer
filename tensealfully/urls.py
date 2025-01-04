from django.urls import path
from .views import set_public_key, input_controller

urlpatterns = [
    path('setpbk/', set_public_key, name='set-public-key'),
    path('input-controller/', input_controller, name='input-controller')
]
