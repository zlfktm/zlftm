from django.db import models

from config.models import BaseModel


DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

class Restaurant(BaseModel) :
    name = models.CharField("이름", max_length=50)
    address = models.CharField("주소", max_length=200)
    contact = models.CharField("연락처", max_length=50)
    open_time = models.TimeField("영업 시작", null=True, blank=True)
    close_time = models.TimeField("영업 마감", null=True, blank=True)
    last_order = models.TimeField("마지막 주문", null=True, blank=True)
    regular_holiday = models.CharField("휴무", choices=DAYS_OF_WEEK, null=True, blank=True, max_length=10)
