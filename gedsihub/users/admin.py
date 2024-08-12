from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Student, Employee

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('is_superuser', 'is_staff')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'college', 'program', 'year', 'section')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Ensure superuser employees can see all students
        if request.user.is_superuser:
            return qs
        # Ensure only admin users can see this list
        if not request.user.is_superuser:
            qs = qs.none()
        return qs

    def has_change_permission(self, request, obj=None):
        # Allow superusers to change any student record
        if request.user.is_superuser:
            return True
        # Restrict to admin users otherwise
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Allow superusers to delete any student record
        if request.user.is_superuser:
            return True
        # Restrict to admin users otherwise
        return super().has_delete_permission(request, obj)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'branch_office_section_unit', 'position', 'sector')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Allow superuser employees to see all employees
        if request.user.is_superuser:
            return qs
        # Ensure only employees with specific permissions can see this list
        if not request.user.has_perm('app.can_view_employees'):
            qs = qs.none()
        return qs

    def has_change_permission(self, request, obj=None):
        # Allow superusers to change any employee record
        if request.user.is_superuser:
            return True
        # Only allow employees with the right permission to change
        if request.user.has_perm('app.can_change_employee'):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        # Allow superusers to delete any employee record
        if request.user.is_superuser:
            return True
        # Only allow employees with the right permission to delete
        if request.user.has_perm('app.can_delete_employee'):
            return True
        return False

    def has_module_permission(self, request):
        # Allow superuser employees to access the admin module
        if request.user.is_superuser:
            return True
        # Otherwise, check specific permissions for regular employees
        return super().has_module_permission(request)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Employee, EmployeeAdmin)
