from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminRole(BasePermission):
    message = "Only admin users can perform this action."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.role == "ADMIN")
        )


class IsAdminOrTeacherRole(BasePermission):
    message = "Only admins or teachers can perform this action."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.role in ["ADMIN", "TEACHER"])
        )


class IsAdminWriteOrAuthenticatedRead(BasePermission):
    message = "Only admins can modify this resource."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.role == "ADMIN")
        )
