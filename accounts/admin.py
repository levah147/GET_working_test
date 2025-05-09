from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.translation import gettext_lazy as _

# from .models import User, AdministratorProfile

# class UserAdmin(BaseUserAdmin):
#     """Define admin model for custom User model with no username field."""
    
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number')}),
#         (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
#                                        'groups', 'user_permissions')}),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2'),
#         }),
#     )
#     list_display = ('email', 'first_name', 'last_name', 'is_staff')
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('email',)
    
#     def get_user_type(self, obj):
#         """Return the user type (Company, Administrator, or Regular)."""
#         if obj.is_company():
#             return 'Company'
#         elif obj.is_administrator():
#             return 'Administrator'
#         else:
#             return 'Regular'
    
#     get_user_type.short_description = 'User Type'
    
#     # Add the get_user_type method to list_display
#     list_display = ('email', 'first_name', 'last_name', 'get_user_type', 'is_staff')

# class AdministratorProfileAdmin(admin.ModelAdmin):
#     """Admin configuration for AdministratorProfile model."""
#     list_display = ('user', 'department', 'position', 'employee_id', 'date_appointed')
#     search_fields = ('user__email', 'user__first_name', 'user__last_name', 'department', 'position')
#     list_filter = ('department', 'date_appointed')

# # Register the models
# admin.site.register(User, UserAdmin)
# admin.site.register(AdministratorProfile, AdministratorProfileAdmin)