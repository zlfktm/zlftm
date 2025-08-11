from django.test import TestCase
from users.models import User

class UserModelTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            nickname="test",
            email="test@test.com",
            password="test123",
        )
        User.objects.create_superuser(
            nickname="supertest",
            email="super@test.com",
            password="super123",
        )

    def test_user_manager_create_user(self):
        new_user = User.objects.get(nickname="test")

        self.assertEqual(new_user.email, "test@test.com")
        self.assertEqual(new_user.profile_image, "users/blank_profile_image.png")
        self.assertEqual(new_user.is_superuser, False)


    def test_user_manager_create_superuser(self):
        new_super_user = User.objects.get(nickname="supertest")

        self.assertEqual(new_super_user.email, "super@test.com")
        self.assertEqual(new_super_user.profile_image, "users/blank_profile_image.png")
        self.assertEqual(new_super_user.is_superuser, True)