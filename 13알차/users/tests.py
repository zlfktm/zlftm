from django.test import TestCase
from django.urls.base import reverse

from rest_framework.test import APITestCase
from rest_framework import status

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


class UserAPIViewTestCase(APITestCase) :
    def setUp(self):
        self.user_info = {
            "nickname": "test",
            "email" : "test@test.com",
            "password" : "test-password1234",
        }

    def test_user_signup(self):
        response = self.client.post(reverse('user-signup'), self.user_info, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data.get('nickname'), self.user_info['nickname'])
        self.assertEqual(response.data.get('email'), self.user_info['email'])

    def test_user_login(self):
        user = User.objects.create_user(**self.user_info)
        login_data = {
            'email' : user.email,
            'password' : 'test-password1234',
        }

        response = self.client.post(reverse('user-login'), login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'), 'User logged in')

    def test_user_login_invalid_credentials(self):
        user = User.objects.create_user(**self.user_info)
        login_data = {
            'email' : "wrong@test.com",
            'password' : 'wrong-password',
        }

        response = self.client.post(reverse('user-login'), login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_details(self):
        user = User.objects.create_user(**self.user_info)
        self.client.login(email=self.user_info['email'], password=self.user_info['password'])

        response = self.client.get(reverse('user-detail', kwargs={'pk':user.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('nickname'), self.user_info['nickname'])
        self.assertEqual(response.data.get('email'), self.user_info['email'])

    def test_update_user_details(self):
        user = User.objects.create_user(**self.user_info)
        self.client.login(username=self.user_info['email'], password=self.user_info['password'])
        update_data = {
            'nickname' : "update-test",
            'email' : 'update@test.com',
            'password' : "updated-password",
        }

        response = self.client.put(reverse('user-detail', kwargs={'pk':user.id}), data=update_data)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('nickname'), update_data['nickname'])
        # self.assertEqual(response.data.get('password'), update_data['password'])

    def test_delete_user(self):
        user = User.objects.create_user(**self.user_info)
        self.client.login(email=self.user_info['email'], password=self.user_info['password'])

        response = self.client.delete(reverse('user-detail', kwargs={'pk':user.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(email=self.user_info['email']).exists())