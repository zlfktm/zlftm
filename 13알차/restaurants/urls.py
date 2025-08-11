from django.urls.conf import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(f'restaurants', views.RestaurantViewSet, basename='restaurant')
