from django.urls import path

from intern_app.views import user_views

from rest_framework_simplejwt.views import (TokenRefreshView, )



urlpatterns = [


    # URL for Registration
    path('register/', user_views.RegisterView.as_view(), name="register"),

    # URL for logging in the user
    path('login/', user_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # URL for generating/refreshing the tokens, when access token expires
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # URL for logging out the user
    path('logout/', user_views.LogoutView.as_view(), name="logout"),

    
]



