from django.db import models
from django.db.models.fields.related import ForeignKey

from config.models import BaseModel
from restaurants.models import Restaurant
from users.models import User


class Review(BaseModel) :
    user = ForeignKey(User, on_delete=models.CASCADE)
    restaurant = ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    comment = models.TextField("본문")
