from rest_framework.permissions import BasePermission

class RestaurantOwnerShipPermission(BasePermission):

    message = "Permission denied for manipulating restaurants !"

    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_merchant

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or obj.res_user == request.user


class MerchantViewPermission(BasePermission):

    message = "Permission denied for viewing restaurants !"

    def has_permission(self, request, view):
        if request.user.is_merchant and request.method == "GET":
            return False
        return request.user.is_admin or request.user.is_merchant