from rest_framework import permissions

from users.models import Role


class StudentsOnly(permissions.BasePermission):
    message = 'This endpoint for STUDENTS only.'

    def has_permission(self, request, view):
        user = request.user
        role = Role.objects.get(id=Role.STUDENT)
        if role in user.roles.all():
            return True
        return False


class OwnerOnly(permissions.BasePermission):
    message = 'OWNER only endpoint.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class SupervisorsOnly(permissions.BasePermission):
    message = 'This endpoint for SUPERVISORS only.'

    def has_permission(self, request, view):
        user = request.user
        role = Role.objects.get(id=Role.SUPERVISOR)
        if role in user.roles.all():
            return True
        return False
