""" API url configuration """
from django.urls import path

from .views.auth import AuthApi
from .views.auth import NewPasswordApi
from .views.auth import RefreshTokenApi

urlpatterns = [
    path('auth/', AuthApi.as_view(), name='authentication'),
    path('change_password/<int:user_pk>', NewPasswordApi.as_view(), name='change_password'),
    path('refresh_token/', RefreshTokenApi.as_view(), name='refresh_token'),
]