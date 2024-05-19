from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
# Create your views here.
@api_view(['GET'])
def ping(request):
    return Response(status=200, data = {
        "timestamp": datetime.datetime.now()
    })