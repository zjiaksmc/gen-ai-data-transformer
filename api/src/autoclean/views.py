import os
import sys
import redis
import pickle
import json
import ast
from uuid import uuid4
import requests
import hashlib

from django.shortcuts import render
from django.conf import settings

from rest_framework.generics import GenericAPIView
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.serializers import Serializer
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class JobList(GenericAPIView):
    """
    Retrieve list of jobs from Airflow logs
    """
    serializer_class = Serializer
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'created_dt',
                openapi.IN_QUERY,
                description="Creation timestamp of the job",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Status of the job",
                type=openapi.TYPE_STRING,
            )
        ],
    )
    def get(self, request):
        """
        Retrieve all autocleansing jobs
        """
        try:
            return Response({}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message":"Error when retrieving jobs: {}".format(sys.exc_info())},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        """
        Create a autocleansing job
        """
        try:
            return Response({}, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {"message":"Error when creating jobs: {}".format(sys.exc_info())},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class JobDetail(GenericAPIView):
    """
    Manage a single job
    """
    serializer_class = Serializer
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """
        Retrieve a job
        """
        try:
            return Response({}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message":"Error when retrieving job {}: {}".format(id, sys.exc_info())},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, id):
        """
        Delete a job
        """
        try:
            return Response({"message": "Successfully remove the job"}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(
                {"message":"Error when deleting job {}: {}".format(id, sys.exc_info())},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, id):
        """
        Update a job
        """
        try:
            return Response({"message": "Successfully update the job"}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(
                {"message":"Error when updating job {}: {}".format(id, sys.exc_info())},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        