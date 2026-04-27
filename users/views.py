from django.shortcuts import render

# Create your views here.
# apps/users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_or_create_user_from_psid
from .utils import generate_tokens

class PSIDLoginView(APIView):
    def post(self, request):
        psid = request.data.get("psid")

        if not psid:
            return Response({"error": "PSID required"}, status=400)

        user = get_or_create_user_from_psid(psid)
        tokens = generate_tokens(user)

        return Response(tokens)