from rest_framework.response import Response
from rest_framework import authentication, permissions

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from rest_framework import status, viewsets
from rest_framework.decorators import action

from django.db.models import Q
from intern_app.serializers import TaskSerializer
from ..models import User, Task
from ..permissions import IsAssignee

from drf_yasg.utils import swagger_auto_schema  



class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAssignee]
    model = Task
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'

    @swagger_auto_schema(operation_summary = "Get the list of tasks.")
    def list(self, request):
        """
            This url requires does not requires any parameter.
        """
        tasks = self.model.objects.filter(Q(assignee=request.user) | Q(assignor=request.user))
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    

    @swagger_auto_schema(operation_summary = "Get particular task.")
    def retrieve(self, request, id):
        """
            This url only requires id as url parameter.
        """
        task = self.model.objects.get(id=id)

        if task:
            if task.assignee == request.user or request.user.is_superuser:
                serializer = self.serializer_class(task)
                return Response(serializer.data, status= status.HTTP_200_OK)
            
            return Response({'error': 'Unauthroized to access the task'}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({'error': 'Task does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        

    @swagger_auto_schema(operation_summary = "Supervisor/Admin can only add a Task")
    def create(self, request):
        """
            This url requires following data in post request:
            ```
                tasktitle: string (required)
                assignee: integer (required)
                assignor: integer
                is_completed: boolean (required)
            ```
        """
        if request.user.is_superuser or request.user.is_supervisor:

            request.data['assignor'] = request.user.id
            serializer = self.serializer_class(data= request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    status= status.HTTP_201_CREATED,
                    data= serializer.data
                    )
            
            return Response(
                data= serializer.errors,
                status= status.HTTP_400_BAD_REQUEST
                )
        
        else:
            return Response({'error': 'Unauthroized to create the task'}, status=status.HTTP_403_FORBIDDEN)
    

    @swagger_auto_schema(operation_summary = "Supervisor can only fully update a Task")
    def update(self, request, id=None):
        """
            This url only requires id as url parameter and following data in put request:
            ```
                tasktitle: string (required)
                assignee: integer (required)
                assignor: integer
                is_completed: boolean (required)
            ```
        """
        task = self.model.objects.get(id=id)

        if task:
            if task.assignor == request.user:
                request.data['assignor'] = request.user.id
                
                serializer=self.serializer_class(task, data= request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(data = serializer.data, status = status.HTTP_200_OK)


                return Response(data=serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            
            return Response({'error': 'Only Supervisor can fully update the Task. Intern can only partial update the task.'}, status=status.HTTP_403_FORBIDDEN)

        return Response({'error': 'Task does not exist'}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(operation_summary = "Intern can only partially update a Task")
    def partial_update(self, request, id=None):
        """
            This url only requires id as url parameter and following data in patch request:
            ```
                is_completed: boolean (required)
            ```
        """
        task = self.model.objects.get(id=id)

        if task:

            if task.assignee == request.user:
                request.data['tasktitle'] = task.tasktitle
                request.data['assignor'] = task.assignor.id
                request.data['assignee'] = task.assignee.id

                serializer = self.serializer_class(task, data= request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(data = serializer.data, status = status.HTTP_200_OK)

                return Response(data=serializer.errors, status = status.HTTP_400_BAD_REQUEST)

            return Response({'error': 'Only task assignee can mention task completion'}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({'error': 'Task does not exist'}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(operation_summary = "Only Supervisor can delete a Task")
    def destroy(self, request, id=None):
        """
            This url only requires id as url parameter and delete request should be called.
        """
        task = self.model.objects.get(id=id)

        if task:
            if task.assignor == request.user:
                task.delete()
                return Response(status = status.HTTP_204_NO_CONTENT)
            
            return Response({'error': 'Only Supervisor can delete the task'}, status=status.HTTP_403_FORBIDDEN)

        return Response({'error': 'Task does not exist'}, status=status.HTTP_400_BAD_REQUEST)




            
    









   





