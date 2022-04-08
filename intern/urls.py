from django.contrib import admin
from django.urls import path, include


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# For Swagger UI (openapi)
schema_view = get_schema_view(
   openapi.Info(
      title="Intern Management System",
      default_version='v1',
      description="APIs for Intern Management System (Task assignment & Attendance)",
      terms_of_service="https://www.ourapp.com/policies/terms/",
      contact=openapi.Contact(email="contact@drf.local"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [

   # URL for inbuilt Admin Panel
   path('admin/', admin.site.urls),

    
   



   # yo talako sabai url haru swagger & redoc ko lagi ho
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('api/api.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]



