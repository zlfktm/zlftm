from django.test import TestCase
from django.urls.base import reverse

from rest_framework.test import APITestCase

from reviews.models import Review
from users.models import User
from restaurants.models import Restaurant


class ReviewModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            nickname="test-user",
            email="test@test.com",
            password="test123",
        )
        restaurant = Restaurant.objects.create(
            name = "test-restaurant",
            address = "test-address",
            contact = "test-contact",
        )

        Review.objects.create(
            user = user,
            restaurant = restaurant,
            title = "test",
            comment = "test-comment",
        )

    def test_create_review(self):
        new_review = Review.objects.get(title="test")

        self.assertEqual(new_review.user.nickname, "test-user")
        self.assertEqual(new_review.restaurant.name, "test-restaurant")
        self.assertEqual(new_review.comment, "test-comment")


class ReviewAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            nickname="test-user",
            email="test@test.com",
            password="test123",
        )
        self.restaurant = Restaurant.objects.create(
            name = "test-restaurant",
            address = "test-address",
            contact = "test-contact",
        )

        self.review_info = {
            "user" : self.user,
            "restaurant" : self.restaurant,
            "title" : "test",
            "comment" : "test-comment",
        }

    def test_get_review_list(self):
        review = Review.objects.create(**self.review_info)
        response = self.client.get(reverse('review-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertEqual(response.data.get('results')[0].get('title'), self.review_info['title'])
        self.assertEqual(response.data.get('results')[0].get('comment'), self.review_info['comment'])
        self.assertEqual(response.data.get('results')[0].get('user')['id'], self.review_info['user'].id)
        self.assertEqual(response.data.get('results')[0].get('restaurant')['id'], self.review_info['restaurant'].id)

    def test_post_review(self):
        response = self.client.post(reverse('review-list'), self.review_info)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('results').get('title'), self.review_info['title'])
        self.assertEqual(response.data.get('results').get('comment'), self.review_info['comment'])
        self.assertEqual(response.data.get('results').get('user')['id'], self.review_info['user'].id)
        self.assertEqual(response.data.get('results').get('restaurant')['id'], self.review_info['restaurant'].id)

    def test_get_review_detail(self):
        review = Review.objects.create(**self.review_info)
        response = self.client.get(reverse('review-detail', kwargs={'pk': review.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('title'), self.review_info['title'])
        self.assertEqual(response.data.get('comment'), self.review_info['comment'])
        self.assertEqual(response.data.get('user')['id'], self.review_info['user'].id)
        self.assertEqual(response.data.get('restaurant')['id'], self.review_info['restaurant'].id)

    def test_update_review(self):
        review = Review.objects.create(**self.review_info)

        update_data = {
            "title" : "update-title",
            "comment" : "update-comment",
        }

        response = self.client.put(reverse('review-detail', kwargs={'pk': review.id}), update_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('title'), update_data['title'])
        self.assertEqual(response.data.get('comment'), update_data['comment'])

    def test_delete_review(self):
        review = Review.objects.create(**self.review_info)

        response = self.client.delete(reverse('review-detail', kwargs={'pk': review.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Review.objects.filter(email=self.review_info['email']).exists())