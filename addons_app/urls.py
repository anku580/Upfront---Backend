# django imports
from django.urls import path

# project imports
from addons_app.views.restaurant_offer_view import RestaurantOfferView
from addons_app.views.admin_offer_view import AdminOfferView
from addons_app.views.admin_offer_detail_view import AdminOfferDetailView
from addons_app.views.restaurant_offer_detail_view import RestaurantOfferDetailView
from addons_app.views.addons import offerManipulationInMenu,bulkOfferManipulation

urlpatterns = [
    path('restaurants/<int:resid>/offers',RestaurantOfferView.as_view(),),
    path('restaurants/<int:resid>/offers/<int:offerid>', RestaurantOfferDetailView.as_view(), ),
    path('promotions',AdminOfferView.as_view()),
    path('promotions/<int:id>',AdminOfferDetailView.as_view(),),
    path('restaurants/<int:resid>/offers/<int:offerid>/menus/<int:menuid>',offerManipulationInMenu),
    path('restaurants/<int:resid>/offers/<int:offerid>/bulk',bulkOfferManipulation)
]


