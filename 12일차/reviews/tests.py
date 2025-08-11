from django.test import TestCase
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