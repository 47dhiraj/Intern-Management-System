from django.shortcuts import render, redirect

from ..models import User
from django.urls import reverse
from django.contrib.auth import authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from rest_framework.response import Response
from rest_framework import generics, status, views, permissions
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

import jwt

from ..serializers import RegisterSerializer, UserSerializerWithToken, LogoutSerializer

from drf_yasg.utils import swagger_auto_schema                                                          # swagger ko auto schema ko laig import gareko
from drf_yasg import openapi                                                                            # openapi lai import gareko



# Create your views here.

class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @swagger_auto_schema(operation_summary = "Register user by signing up.")
    def post(self, request):
        """
            ## Register/Create a new user.

            This url requires the following input paramters :
            ```
                username: string
                email: string
                password: string
            ```
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)                                               
        serializer.save()                                                                      
        user_data = serializer.data

        user_data['detail']= 'Registered successfully' 
        return Response(user_data, status=status.HTTP_201_CREATED)
        


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)          

        if data:
            data.pop('refresh', None)
            data.pop('access', None)
        
        serializer = UserSerializerWithToken(self.user).data
    
        for k, v in serializer.items():
            data[k] = v

        return data
    


class MyTokenObtainPairView(TokenObtainPairView):       
    """
        Login to the system.

        This url requires two input paramters:
        ```
            email: string
            password: string
        ```
    """
    serializer_class = MyTokenObtainPairSerializer
    

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(operation_summary = "Logout from system.")
    def post(self, request):
        """
            Logout from the system.

            This url requires single input parameter:
            ```
                refresh: string
            ```
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)                               
        serializer.save()                                                       

        return Response(status = status.HTTP_204_NO_CONTENT)








