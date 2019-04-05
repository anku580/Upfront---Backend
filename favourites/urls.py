from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views.FavouriteRestaurantsView import FavouriteRestaurantsView
from .views.FavouriteMenusView import FavouriteMenusView
from .views.CheckFavouriteRestaurantView import CheckFavouriteRestaurantView
from .views.CheckFavouriteMenuView import CheckFavouriteMenuView


urlpatterns = [
   
    path('res/add',FavouriteRestaurantsView.as_view(),name="favresadd"),
    path('res/delete/<int:id>',FavouriteRestaurantsView.as_view(),name="favresdelete"),
    path('res/check/<int:id>',CheckFavouriteRestaurantView.as_view(),name="favrescheck"),

    path('menu/add',FavouriteMenusView.as_view(),name="favmenuadd"),
    path('menu/delete/<int:id>',FavouriteMenusView.as_view(),name="favmenudelete"),
    path('menu/check/<int:id>',CheckFavouriteMenuView.as_view(),name="favmenudelete"),



    

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])