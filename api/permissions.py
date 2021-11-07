from rest_framework import permissions


class IsAdministrator(permissions.BasePermission):
    """проверает является ли юзер админом или суперюзером"""
    def has_permission(self, request, view):
        return request.user.is_admin


class IsModerator(permissions.BasePermission):
    """
    Проверяет является ли пользователь модератором
    """
    def has_permission(self, request, view):
        return request.user.is_moderator


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    """Позволяет GET всем, POST только Аутентифицированному пользователю
    но PPD только автору, модератору или админу"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        is_staff = (request.user.is_authenticated
                    and (request.user.is_admin
                         or request.user.is_moderator))
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user or is_staff)


class IsAdministratorOrReadOnly(permissions.BasePermission):
    """Позволяет GET всем но PPPD только админу и суперюзеру"""

    def has_permission(self, request, view):
        is_admin = (request.user.is_authenticated
                    and request.user.is_admin)
        return request.method in permissions.SAFE_METHODS or is_admin
