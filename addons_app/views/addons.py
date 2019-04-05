
# django imports
from rest_framework.decorators import api_view
from rest_framework.response import Response

# project imports
from menu_app.models import Menu
from addons_app.models import RestaurantOffer
from addons_app import custom_messages

def applyOfferToMenu(menuid,offerid):
    offer_obj = RestaurantOffer.objects.get(id=offerid)
    menu_obj = Menu.objects.get(id=menuid)
    discount_price = (menu_obj.original_price * offer_obj.discount_percentage)/100
    menu_obj.discounted_price = menu_obj.original_price - discount_price
    menu_obj.offer_id = offer_obj
    menu_obj.save()

def removeOfferFromMenu(menuid):
    menu_obj = Menu.objects.get(id=menuid)
    menu_obj.discounted_price = menu_obj.original_price
    menu_obj.offer_id = None
    menu_obj.save()

@api_view(['POST','DELETE'])
def offerManipulationInMenu(request,resid,offerid,menuid):
    if request.method == "POST":
        json_response_obj = {}
        applyOfferToMenu(menuid,offerid)
        json_response_obj['message'] = custom_messages.OFFER_APPLIED_MENU_SUCCESS_MSG
        return Response(json_response_obj)
    elif request.method == "DELETE":
        json_response_obj = {}
        removeOfferFromMenu(menuid, offerid)
        json_response_obj['message'] = custom_messages.OFFER_UNAPPLIED_SUCCESS_MSG
        return Response(json_response_obj)

@api_view(['POST','DELETE'])
def bulkOfferManipulation(request,resid,offerid):
    json_response_obj = {}
    if request.method == "POST":
        for menu in Menu.objects.filter(res_id=resid):
            applyOfferToMenu(menu.id,offerid)
        json_response_obj['message'] = custom_messages.OFFER_APPLIED_MENU_SUCCESS_MSG
        return Response(json_response_obj)

    elif request.method == "DELETE":
        for menu in Menu.objects.filter(res_id=resid):
            removeOfferFromMenu(menu.id)
        json_response_obj['message'] = custom_messages.OFFER_UNAPPLIED_SUCCESS_MSG
        return Response(json_response_obj)