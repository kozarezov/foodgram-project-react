from rest_framework.permissions import (SAFE_METHODS,
                                        BasePermission,
                                        IsAuthenticatedOrReadOnly,)


class IsOwnerOrAdminOrReadOnly(BasePermission):
    """Проверка, что пользователь является автором или админом."""

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.user.is_superuser:
            return True
        return request.user == obj.author


class IsAuthorOrStaffOrReadOnly(IsAuthenticatedOrReadOnly):
    """Проверка, что пользователь является автором или стафом."""
    def has_object_permission(self, request, view, obj):
        return (
            request.method in ('GET',)
            or (request.user == obj.author)
            or request.user.is_staff
        )
