from django.urls.conf import path

from reviews import views

urlpatterns = [
    path('restaurants/<int:restaurant_id>/reviews', views.ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<int:review_id>', views.ReviewDetailView.as_view(), name='review-detail'),
]