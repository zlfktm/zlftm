from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.fields.files import ImageField
from django.db.models.manager import BaseManager


class UserManager(BaseUserManager) :
    def create_user(self, nickname, email, password, *args, **kwargs):
        if not email :
            raise ValueError('올바른 이메일을 입력하세요.')

        user = self.model(
            email = self.normalize_email(email),
            nickname = nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, email, password, *args, **kwargs):
        user = self.create_user(nickname, email, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin) :
    nickname = models.CharField("닉네임", max_length=20, unique=True)
    email = models.EmailField("이메일", max_length=40, unique=True)
    profile_image = ImageField("프로필 이미지", upload_to="users/profile_images", default="users/blank_profile_image.png")

    objects = UserManager()
    USERNAME_FIELD = "email"