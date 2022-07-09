from rest_framework import permissions

class IsUser(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
       
        return obj == request.user

class IsAdmin(permissions.BasePermission):
    
    def has_admin_permission(self, request, view):
       
        return request.user.is_staff == 1