# apps/users/urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import include, path


from users.views import FacebookLogin, GoogleLogin, PSIDLoginView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    
    path('psid-login/', PSIDLoginView.as_view()),
    
    path('api/auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    
]