##creating our custom permissions 
from rest_framework import permissions 

class isAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "ADMIN" 
    
class IsLibrarianOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ["LIBRARIAN", "ADMIN"]

class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "MEMBER"