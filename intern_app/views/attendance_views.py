from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

from ..models import User, Attendance
from intern_app.serializers import UserSerializer, AttendanceSerializer

from drf_yasg.utils import swagger_auto_schema                                                          # swagger ko auto schema ko laig import gareko



@swagger_auto_schema(method='GET')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAttendances(request):

    if request.user.is_staff == True:
        if request.method == 'GET':
            attendances = Attendance.objects.all()
            serializer = AttendanceSerializer(attendances, many=True)
            return Response(serializer.data) 


    user = request.user
    # attendances = user.attendance_set.all()                       # if not mentioned related_name in models file
    attendances = user.attendant.all()                              # if related_name is mentioned in models file then, can only use related_name to acces child objects
    serializer = AttendanceSerializer(attendances, many=True)
    return Response(serializer.data)




@swagger_auto_schema(method='POST', request_body=AttendanceSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])                              # only authenticated user can do attendance
def doAttendance(request):
    
    if request.user.id == request.data['user']:
        request.data['user'] = request.user.id
        serializer = AttendanceSerializer(data= request.data)

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

    return Response({'error': 'Invalid user or Attendance of another user cannot be done'}, status=status.HTTP_403_FORBIDDEN)



