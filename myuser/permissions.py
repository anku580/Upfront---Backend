from rest_framework import permissions

class AdminAllowedPermission(permissions.BasePermission):

	message = 'only admin is allowed'
	def has_permission(self, request, view):
		if request.user.is_admin:
			return True
		return False

class MerchantAllowedPermission(permissions.BasePermission):

	message = 'only merchant is allowed'
	def has_permission(self, request, view):
		if request.user.is_merchant:
			return True
		return False
class CustomerAllowedPermission(permissions.BasePermission):

	message = 'only customer is allowed'
	def has_permission(self, request, view):
		if request.user.is_customer:
			return True
		return False
class SubadminAllowedPermission(permissions.BasePermission):

	message = 'only subadmin is allowed'
	def has_permission(self, request, view):
		if request.user.is_subadmin:
			return True
		return False
class SubadminNotAllowedPermission(permissions.BasePermission):

	message = 'subadmin is not allowed'
	def has_permission(self, request, view):
		if request.user.is_subadmin:
			return False
		return True

class UserActivation(permissions.BasePermission):

	message = 'only activated users are allowed'
	def has_permission(self, request, view):
		if request.user.is_activated:
			return False
		return True