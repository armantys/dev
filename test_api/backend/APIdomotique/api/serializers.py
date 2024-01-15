# serializers.py

from rest_framework import serializers
from .models import lieux, capteurs, comparaison_api, donneesMeteo

class lieuxSerializer(serializers.ModelSerializer):
    class Meta:
        model = lieux
        fields = '__all__'

class capteursSerializer(serializers.ModelSerializer):
    class Meta:
        model = capteurs
        fields = '__all__'

class comparaisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = comparaison_api
        fields = '__all__'

class donneesMeteoSerializer(serializers.ModelSerializer):
    class Meta:
        model = donneesMeteo
        fields = '__all__'