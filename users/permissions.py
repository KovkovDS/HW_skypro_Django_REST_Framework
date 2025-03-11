from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Модератор").exists()


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


# class IsUser(BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         if request.user.has_perm('IsAuthenticated'):
#             view in ['create']
#         return False


class IsAdministrator(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Администратор").exists()
