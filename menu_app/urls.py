from django.urls import path
from menu_app.views.category_view import CategoryView
from menu_app.views.category_detail_view import CategoryDetailView
from menu_app.views.menu_view import MenuView
from menu_app.views.menu_detail_view import MenuDetailView
from menu_app.views.addons import MerchantMenuView

urlpatterns = [
    path('restaurants/<int:resid>/menu',MenuView.as_view()),
    path('restaurants/<int:resid>/menu/<int:menuid>',MenuDetailView.as_view()),
    path('restaurants/<int:resid>/category',CategoryView.as_view()),
    path('restaurants/<int:resid>/category/<int:categoryid>',CategoryDetailView.as_view()),

    # custom API URLs
    path('restaurants/<int:resid>/menu/merchantview',MerchantMenuView.as_view())
]