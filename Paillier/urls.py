from django.urls import path
from .views import Controller1
urlpatterns = [
    path('controller1/',Controller1.as_view(),name='Controller1')
]