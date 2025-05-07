from django.contrib.auth.models import AnonymousUser

from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
# from accounts.models import CustomUser


# class IsSubscribed(BasePermission):
# 	message = "the user must be subscribed first"
# 	def has_permission(self, request, view):
# 		return request.user.is_subscribed
