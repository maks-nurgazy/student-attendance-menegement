from rest_framework import permissions

from users.models import Role


class SuperUserOnly(permissions.BasePermission):
    message = 'This endpoint for SuperUser only.'

    def has_permission(self, request, view):
        user = request.user
        role = Role.objects.get(id=Role.SUPERUSER)
        if role in user.roles.all():
            return True
        return False


class AdminOnly(permissions.BasePermission):
    message = 'This endpoint for ADMINS only.'

    def has_permission(self, request, view):
        user = request.user
        role = Role.objects.get(id=Role.ADMIN)
        if role in user.roles.all():
            return True
        return False


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
        print(obj)
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsAttendanceOwner(permissions.BasePermission):
    message = 'ATTENDANCE OWNER only endpoint.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        teacher = obj.teacher
        return user == teacher


class SupervisorsOnly(permissions.BasePermission):
    message = 'This endpoint for SUPERVISORS only.'

    def has_permission(self, request, view):
        user = request.user
        role = Role.objects.get(id=Role.SUPERVISOR)
        if role in user.roles.all():
            return True
        return False


class TeachersOnly(permissions.BasePermission):
    message = 'This endpoint for TEACHERS only.'

    def has_permission(self, request, view):
        user = request.user
        role = Role.objects.get(id=Role.TEACHER)
        if role in user.roles.all():
            return True
        return False
