from django.urls import path
from django.urls import include, re_path

from intern_app.views import user_views, task_views

from rest_framework_simplejwt.views import (TokenRefreshView, )

from rest_framework import permissions


# For extending/using ModelViewSet
from rest_framework.routers import DefaultRouter                            
router = DefaultRouter()                                                   
router.register(r'', task_views.TaskViewSet, basename='task')         



urlpatterns = [

    # URL for Registration
    path('register/', user_views.RegisterView.as_view(), name="register"),

    # URL for Registration
    path('register/admin/', user_views.AdminRegisterView.as_view(), name="register"),

    # URL for logging in the user
    path('login/', user_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # URL for generating/refreshing the tokens, when access token expires
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # URL for logging out the user
    path('logout/', user_views.LogoutView.as_view(), name="logout"),




    re_path(r'^task/', include(router.urls))

    
]


# Root API Path of TaskViewSet ==> http://127.0.0.1:8000/task
# Particular task path ==> http://127.0.0.1:8000/task/pk           # pk vannale primary key (ahile hamro project ko case ma, id chai primary key ho)

