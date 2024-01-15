from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import product
from django.forms.models import model_to_dict
from .forms import ProductSerializer

@api_view(['POST', 'GET'])
def api_view(request):
    #request != requests
    # request est une instance de HttpRequest
    query = product.objects.all().order_by('?').first()
    data = {}
    if query:
        data = ProductSerializer(query).data
       # data = model_to_dict(query, fields=('name', 'content', 'prince', 'get_discount'))
        # serialization: mettre des donnees sous fourme de dictionnaire
    return Response(data)