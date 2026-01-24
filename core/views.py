from django.shortcuts import render

# Create your views here.
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

@extend_schema(responses={200: None})
@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})