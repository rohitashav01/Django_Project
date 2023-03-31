from rest_framework import permissions
from rest_framework.response import Response

edit_methods = ("PUT", "PATCH")

class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff and request.method  in self.edit_methods:
            return True