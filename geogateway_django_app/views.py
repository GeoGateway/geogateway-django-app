from django.http import HttpResponse, FileResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import subprocess
import requests
import zipfile
import io


DislocUrl = 'https://beta.geogateway.scigap.org/geogateway_django_app/disloc'


class MyFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        payload = {
            'file': file
        }
        return FileResponse(requests.get(DislocUrl, params=payload))


class KmlUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']

        return FileResponse(file)


class KmzUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        file = request.FILES['file']
        zip_file = open(file, 'rb')
        return FileResponse(zip_file)
