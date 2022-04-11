from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

from ..models import User, Attendance
from intern_app.serializers import UserSerializer, AttendanceSerializer



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

