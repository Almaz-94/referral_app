from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Check if user is owner of profile"""
    def has_object_permission(self, request, view, obj):
        return request.user == obj
