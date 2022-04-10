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
        

    def create(self, request):
        if request.user.is_superuser or request.user.is_supervisor:

            request.data['assignor'] = request.user.id
            serializer = self.serializer_class(data= request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    status= status.HTTP_201_CREATED,
                    data= serializer.data
                    )
            else:
                return Response(
                    data= serializer.errors,
                    status= status.HTTP_400_BAD_REQUEST
                    )
        
        else:
            return Response({'error': 'Unauthroized to create the task'}, status=status.HTTP_403_FORBIDDEN)
    

    def update(self, request, id=None):
        task = self.model.objects.get(id=id)

        if task.assignor == request.user:
            request.data['assignor'] = request.user.id
            
            serializer=self.serializer_class(task, data= request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(data = serializer.data, status = status.HTTP_200_OK)


            return Response(data=serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'error': 'Only Supervisor can fully update the Task. Intern can only partial update the task.'}, status=status.HTTP_403_FORBIDDEN)

    
    def partial_update(self, request, id=None):
        task = self.model.objects.get(id=id)

        if task.assignee == request.user:
            request.data['tasktitle'] = task.tasktitle
            request.data['assignor'] = task.assignor.id
            request.data['assignee'] = task.assignee.id

            serializer = self.serializer_class(task, data= request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(data = serializer.data, status = status.HTTP_200_OK)

            return Response(data=serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Only task assignee can mention task completion'}, status=status.HTTP_403_FORBIDDEN)



            
    









   





