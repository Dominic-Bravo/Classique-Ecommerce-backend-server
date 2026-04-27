from django.shortcuts import render

# Create your views here.
# apps/users/views.py
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegisterSerializer
from .services import get_or_create_user_from_psid
from .utils import generate_tokens


class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class PSIDLoginView(APIView):
    def post(self, request):
        psid = request.data.get("psid")

        if not psid:
            return Response({"error": "PSID required"}, status=400)

        user = get_or_create_user_from_psid(psid)
        tokens = generate_tokens(user)

        return Response(tokens)