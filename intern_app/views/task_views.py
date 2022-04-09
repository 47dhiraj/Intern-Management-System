from rest_framework.response import Response
from rest_framework import authentication, permissions

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework import status, viewsets
from rest_framework.decorators import action

from intern_app.serializers import TaskSerializer

from ..models import User, Task



# yo talako TaskViewSet vanni class le ModelViewSet lai extend/inherit gareko cha
class TaskViewSet(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication, ]
    # permission_classes = [IsAuthenticated]

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
