from rest_framework.permissions import BasePermission


class IsSectorAgent(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "AGENT"


class IsGovOfficial(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "GOV"
