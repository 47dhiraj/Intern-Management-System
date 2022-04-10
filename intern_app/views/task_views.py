from rest_framework.response import Response
from rest_framework import authentication, permissions

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from rest_framework import status, viewsets
from rest_framework.decorators import action

from django.db.models import Q

from intern_app.serializers import TaskSerializer

from ..models import User, Task

from ..permissions import IsAssignee


# yo talako TaskViewSet vanni class le ModelViewSet lai extend/inherit gareko cha
class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAssignee]
    model = Task
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


    # Overriding inbuilt methods like list(), retrieve(), create(), update(), partial_update(), destroy()

    def list(self, request):
        tasks = self.model.objects.filter(Q(assignee=request.user) | Q(assignor=request.user))
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=200)






