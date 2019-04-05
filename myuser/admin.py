from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyUser, Customer,Merchant,SubAdmin, ConfirmAdmin
# Register your models here.

class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='password',widget=forms.PasswordInput)
	password2 = forms.CharField(label='password_confirmation',widget=forms.PasswordInput)

	class Meta:
		model = MyUser
		fields = ('username','is_customer','is_merchant',)

	def clean_password2(self):
		#Check the two password entries  match

		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")

		if password1 and password2 and password1 != password2 :
			raise forms.ValidationError("passwords don't match")

		return password2

	def save(self, commit =True):
		#save the provided password is hashed format

		user = super(UserCreationForm, self).save(commit = False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class UserChangeForm(forms.ModelForm):
	"""
	A form for updating users.Includes all the fields on the user, but repaces the password field the admins password hash display field.
	"""
	class Meta:
		model = MyUser
		fields = ('username', 'password','is_active', 'is_admin','is_customer','is_merchant',)

	def clean_password(self):
		# regardless of what the user provides, return the initial value.

		#Thos is done here, rather than on the field, because the filed does

		#access to the initial value

		return self.initial['password']

  
class UserAdmin(BaseUserAdmin):
	#The forms to add and user instances

	form = UserChangeForm
	add_form = UserCreationForm

  	#The fields to be used in dispalying the User model.
	#These override the definitions on the base UserAdmin
	
	list_display = ('username','is_admin',)
	list_filter = ('is_admin',)

	
	fieldsets = (
		(None,{'fields':('username','password',),},),
		('personal info', { 'fields': ('is_merchant','is_customer','is_subadmin',),},),
		('permissions',{'fields' : ('is_admin',),},),
	)


	add_fieldsets = (	(None, {
			'classes' : ('wide',),
			'fields' : ('username', 'password1', 'password2','is_customer','is_merchant','is_subadmin',)}
		),

	)

	search_fields = ('username',)
	ordering = ('username',)
	filter_horizontal = ()

# Now register the new UserAdmin

admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Customer)
admin.site.register(Merchant)
admin.site.register(SubAdmin)
admin.site.register(ConfirmAdmin)