# apps/users/urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import include, path


from users.views import (
    FacebookLogin,
    GoogleLogin,
    MyRoleUpdateView,
    PSIDLoginView,
    RegisterView,
    UserListView,
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/me/role/', MyRoleUpdateView.as_view(), name='my-role-update'),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    
    path('psid-login/', PSIDLoginView.as_view()),
    
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    
]
