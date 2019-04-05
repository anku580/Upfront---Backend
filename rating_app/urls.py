# django imports
from django.urls import path

# project imports
from rating_app.views.rating_view import RatingView


urlpatterns = [
    path('orders/<int:order_id>/rating', RatingView.as_view()),
]