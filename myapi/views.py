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
import requests, ast

from ibm_watson import AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Create your views here.

logger = logging.getLogger(__name__)



authenticator = IAMAuthenticator('kLqYFGYfATjuIYDhVmhAaBMZwQ8iz4iXqrfuk0rXL_0B')
service = AssistantV1(
    version='2019-02-28',
    authenticator = authenticator
)
workspace_id='988d1327-d737-48c4-9e3e-a2e35c490db3'

service.set_service_url('https://gateway.watsonplatform.net/assistant/api/')



def index(request):
    return render(request, 'visabot/index.html')



@api_view(["POST"])
def BotProcessRequest(request):
    try:
        logger.info("Request received from IBM watson")
        doc = request.data
        if doc['request_type']== "create_intent":
            url = "https://gateway.watsonplatform.net/assistant/api/v1/workspaces/988d1327-d737-48c4-9e3e-a2e35c490db3/intents?version=2018-09-20"
            payload = {'intent': doc['intent']}
            headers = {
                'content-type': "application/json",
                'authorization': "Basic YXBpa2V5OmtMcVlGR1lmQVRqdUlZRGhWbWhBYUJNWndROGl6NGlYcXJmdWswclhMXzBC",
                'cache-control': "no-cache"
            }
            response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
            print(response)
            res = {"message": "success", "data": request.data}


        elif(doc['request_type'] == "update_intent"):
            print("update intent request")
            print(doc['examples'],type(doc['examples']))
            response = service.update_intent(
                workspace_id=workspace_id, intent=doc['intent'],
                new_examples= ast.literal_eval(doc['examples'])).get_result()
            res = {"message": "success", "data": request.data}

        elif(doc['request_type']== "delete_intent"):
            print('heyyy inside delt api--------------')
            response=service.delete_intent(workspace_id=workspace_id, intent=doc['intent']).get_result()
            print(response.text, indent=2)
            res = {"message": "success", "data": request.data}

        elif(doc['request_type']=="create_entity"):
            print('------------------------')
            print(doc['entity'], doc['values'], type(doc['values']))
            values=[]
            for val in doc['values']:
                values.append({'value': val})
            response = service.create_entity(
                workspace_id=workspace_id,
                entity=doc['entity'],
                values=values
            ).get_result()
            res = {"message": "success", "data": request.data}

        elif (doc['request_type'] == "delete_entity"):
            print('------------------------')
            print(doc['entity'])
            response = service.delete_entity(
                workspace_id=workspace_id,
                entity=doc['entity']
            ).get_result()



        elif(doc['request_type'] == "logs"):
            response = service.list_logs(
                workspace_id=workspace_id
            ).get_result()
            print(response['logs'])
            res = {"message": "success", "logs": response['logs']}


        elif (doc['request_type'] == "fetch_dialogs"):
            print('inside fetch dialogs ----------------------------')
            response = service.list_dialog_nodes(
                workspace_id=workspace_id,
                page_limit=5,
                sort="updated"
            ).get_result()
            print(response)
            res = {"message": "success", "dialog_nodes": response}


        elif(doc['request_type'] == "create_dialog"):
            print(doc['user_input'])
            response = service.create_dialog_node(
                workspace_id= workspace_id,
                dialog_node= doc['df_id'],
                conditions=doc['user_input'][0],
                title=doc['user_input'][1]
            ).get_result()
            print(response)
            res = {"message": "success"}

        elif (doc['request_type'] == "delete_dialog"):
            response = service.delete_dialog_node(
                workspace_id=workspace_id,
                dialog_node=doc['df_id']
            ).get_result()
            print(response)
            res = {"message": "success"}



        else:
            res={'message':'failed'}

        return JsonResponse(res)

    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)
