from django.shortcuts import render
from django.http import JsonResponse
import json
from rest_framework import generics
from .models import lieux, capteurs, comparaison_api, donneesMeteo
from .serializers import lieuxSerializer, capteursSerializer, comparaisonSerializer, donneesMeteoSerializer

class lieuxListView(generics.ListCreateAPIView):
    queryset = lieux.objects.all()
    serializer_class = lieuxSerializer

class capteursListView(generics.ListCreateAPIView):
    queryset = capteurs.objects.all()
    serializer_class = capteursSerializer

class comparaisonListView(generics.ListCreateAPIView):
    queryset = comparaison_api.objects.all()
    serializer_class = comparaisonSerializer

class donneesMeteoListView(generics.ListCreateAPIView):
    queryset = donneesMeteo.objects.all()
    serializer_class = donneesMeteoSerializer
