from django.urls import path
from django.urls import include, re_path

from intern_app.views import user_views, task_views, attendance_views

from rest_framework_simplejwt.views import (TokenRefreshView, )

from rest_framework import permissions


from rest_framework.routers import DefaultRouter                            
router = DefaultRouter()                                                   
router.register(r'', task_views.TaskViewSet, basename='task')         


urlpatterns = [

    path('register/', user_views.RegisterView.as_view(), name="register"),

    path('register/admin/', user_views.AdminRegisterView.as_view(), name="register"),

    path('login/', user_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('logout/', user_views.LogoutView.as_view(), name="logout"),

    path('attendance/', attendance_views.getAttendances, name='attendance'),

    path('attendance/add', attendance_views.doAttendance, name='add_attendance'),
    
    re_path(r'^task/', include(router.urls))
    
]

