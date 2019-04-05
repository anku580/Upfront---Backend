from django.urls import path
from restaurant_app.views.restaurant_view import RestaurantView
from restaurant_app.views.restaurant_detail_view import RestaurantDetailView
from restaurant_app.views.addons import fetchInactiveRestaurant,activateRestaurant,\
    fetchMerchantRestaurants
from restaurant_app.custom_apis.nearby_restaurant_view import NearbyRestaurantView
from restaurant_app.custom_apis.nearby_restaurant_offers_view import NearbyOfferRestaurantsView

urlpatterns=[
    path('restaurants',RestaurantView.as_view(),),
    path('restaurants/<int:resid>',RestaurantDetailView.as_view()),
    path('restaurants/inactive',fetchInactiveRestaurant),
    path('restaurants/<int:resid>/activate',activateRestaurant),
    path('merchant/restaurants',fetchMerchantRestaurants),
    path('restaurants/nearby/normal',NearbyRestaurantView.as_view()),
    path('restaurants/nearby/offers',NearbyOfferRestaurantsView.as_view()),
]
