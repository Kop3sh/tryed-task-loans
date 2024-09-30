from rest_framework import permissions

class OwnsOrIsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of a loan request or admins to view or edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff and request.user.is_superuser:
            return True

        return obj.user == request.user