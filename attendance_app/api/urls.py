from django.contrib import admin
from django.urls import path

from users.api.views.user_login_view import UserLoginView

urlpatterns = [
    path('login/', UserLoginView.as_view())
]
