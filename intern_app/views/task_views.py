from rest_framework.response import Response
from rest_framework import authentication, permissions

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from rest_framework import status, viewsets
from rest_framework.decorators import action

from django.db.models import Q

from intern_app.serializers import TaskSerializer

from ..models import User, Task

from ..permissions import IsAssignee



class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAssignee]
    model = Task
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


    def list(self, request):
        tasks = self.model.objects.filter(Q(assignee=request.user) | Q(assignor=request.user))
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    

    def retrieve(self, request, id):
        task = self.model.objects.get(id=id)

        if task.assignee == request.user or request.user.is_superuser:
            serializer = self.serializer_class(task)
            return Response(serializer.data, status= status.HTTP_200_OK)
        else:
            return Response({'error': 'Unauthroized to access the task'}, status=status.HTTP_403_FORBIDDEN)
        



        











   





  


