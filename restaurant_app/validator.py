from restaurant_app.models import Restaurant
from menu_app.models import Category,Menu

class Validator():

    INVALID_RESTAURANT_MSG = {"message":"Invalid Restaurant ID passed in URL !"}
    INVALID_CATEGORY_MSG = {"message":"Invalid Category ID passed in URL !"}
    INVALID_MENU_MSG = {"message":"Invalid Menu ID passed in URL !"}

    def isValidRestaurant(self,id):
        return Restaurant.objects.filter(id=id).count() != 0

    def isValidCategory(self,id):
        return Category.objects.filter(id=id).count() != 0

    def isValidMenu(self,id):
        return Menu.objects.filter(id=id).count() != 0