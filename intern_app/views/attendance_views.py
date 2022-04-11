from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from datetime import date

from ..models import User, Attendance
from intern_app.serializers import UserSerializer, AttendanceSerializer

from drf_yasg.utils import swagger_auto_schema                                                          



@swagger_auto_schema(method='GET', operation_summary = "Get the attendances of intern.")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAttendances(request):
    """
        This url requires does not requires any parameter.
       
    """
    if request.user.is_staff == True:
        if request.method == 'GET':
            attendances = Attendance.objects.all()
            serializer = AttendanceSerializer(attendances, many=True)
            return Response(serializer.data) 


    user = request.user
    attendances = user.attendant.all()                              
    serializer = AttendanceSerializer(attendances, many=True)
    return Response(serializer.data)




@swagger_auto_schema(method='POST', request_body=AttendanceSerializer, operation_summary = "Add Today's Attendance")
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def doAttendance(request):
    """
        This url requires the following input paramters :
        ```
            user: integer (required)
            work_start_time: string in the format of hh:mm:ss
            work_end_time: string in the format of hh:mm:ss
        ```
    """
    if request.user.id == request.data['user']:

        request.data['user'] = request.user.id
        serializer = AttendanceSerializer(data= request.data)

        if serializer.is_valid():
            attendances = Attendance.objects.filter(user=request.user)

            for attendace in attendances:
                if attendace.date == date.today():
                    return Response({'error': 'Attendance for today has already been done'}, status=status.HTTP_403_FORBIDDEN)
                    
            serializer.save()

            return Response(
                status= status.HTTP_201_CREATED,
                data= serializer.data
                )
        
        return Response(
            data= serializer.errors,
            status= status.HTTP_400_BAD_REQUEST
            )

    return Response({'error': 'Invalid user or Attendance of another user cannot be done'}, status=status.HTTP_403_FORBIDDEN)



