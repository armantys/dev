from rest_framework import serializers

from .models import product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ('name', 'content', 'prince', 'get_discount')
    