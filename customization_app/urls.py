from django.urls import path

# project imports
from customization_app.views.customization_view import CustomizationView
from customization_app.views.customization_detail_view import CustomizationDetailView
from customization_app.views.menu_customization_view import MenuCustomizationView


urlpatterns = [
    path('restaurants/<int:resid>/customizations',CustomizationView.as_view()),
    path('restaurants/<int:resid>/customizations/<int:cus_id>',CustomizationDetailView.as_view()),
    path('menu/<int:menu_id>/customizations/<int:cus_id>/customize',MenuCustomizationView.as_view())
]