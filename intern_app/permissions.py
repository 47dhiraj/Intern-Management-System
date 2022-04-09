from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAssignee(BasePermission):
    """
        Custom permission to check if the user is supervisor or assignee of the task object. 
    """
    message = "Unauthorized to perform this action"

    def has_permission(self, request, view):
        print(request.user.is_authenticated)
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.assignee == request.user or obj.assignor.is_supervisor == True
