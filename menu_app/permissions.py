from rest_framework.permissions import BasePermission

class CategoryOwnershipPermission(BasePermission):

    message = "Permission denied for manipulating category !"

    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_merchant

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or obj.res_id.res_user == request.user


class MenuOwnershipPermission(BasePermission):

    message = "Permission denied for manipulating menu !"

    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_merchant

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or obj.res_id.res_user == request.user

