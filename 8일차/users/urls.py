from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic.base import TemplateView

from users import cb_views as user_views

urlpatterns = [
    path('signup/', user_views.SignupView.as_view(), name='users_signup'),
    path('login/', user_views.LoginView.as_view(), name='users_login'),
    path('logout/', LogoutView.as_view(), name='users_logout'),
    path('verify/', user_views.verify_email, name='users_verify_email'),
]