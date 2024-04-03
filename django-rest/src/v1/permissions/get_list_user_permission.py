from rest_framework import permissions

class GetListUserPermission(permissions.BasePermission):
    """
    Custom permission to only allow staff to view all users, and users to view themselves.
    """

    def has_permission(self, request, view):
        # Allow list requests only to staff
        if view.action == 'list':
            return request.user and request.user.is_employee
        return True

    def has_object_permission(self, request, view, obj):
        # Allow detailed view to staff or the user itself
        return request.user and (request.user.is_employee or request.user == obj)