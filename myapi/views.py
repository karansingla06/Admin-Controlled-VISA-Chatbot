from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
import logging
import requests
# Create your views here.

logger = logging.getLogger(__name__)


@api_view(["POST"])
def BotProcessRequest(request):
    try:
        logger.info("Request received from IBM watson")
        doc = request.data
        if doc['request_type']== "intent":
            url = 'https://gateway.watsonplatform.net/assistant/api/v1/workspaces/988d1327-d737-48c4-9e3e-a2e35c490db3/'
            myobj = {'intent': 'testing1'}
            header= {"Content-Type":"application/json"}
            x = requests.post(url, auth = ('apikey', 'Basic kLqYFGYfATjuIYDhVmhAaBMZwQ8iz4iXqrfuk0rXL_0B'), json=myobj, headers=header)
            res = {"message": "success", "data": request.data}
        else:
            res = {"message": "failed", "data": request.data}

        return JsonResponse(res)
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)
