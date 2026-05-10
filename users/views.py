# apps/users/views.py
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    PSIDLoginSerializer,
    RegisterSerializer,
    RoleUpdateSerializer,
    UserSerializer,
)
from .services import get_or_create_user_from_psid
from .utils import generate_tokens

User = get_user_model()

# register endpoint
class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

ntiopdne
class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class MyRoleUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = RoleUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'head', 'options']

    def get_object(self):
        return self.request.user


class PSIDLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PSIDLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_or_create_user_from_psid(serializer.validated_data["psid"])
        tokens = generate_tokens(user)

        return Response(tokens)
    
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/google-callback"
    client_class = OAuth2Client
    

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    callback_url = "http://localhost:3000/facebook-callback"
    client_class = OAuth2Client 
