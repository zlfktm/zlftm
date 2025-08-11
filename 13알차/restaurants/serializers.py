from django.contrib.auth import get_user_model
from rest_framework import serializers

from restaurants.models import Restaurant

User = get_user_model()

class RestaurantSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Restaurant
        fields = '__all__'