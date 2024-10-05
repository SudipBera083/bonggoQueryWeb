# myapp/serializers.py
from rest_framework import serializers

class MyDataSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=100)
    
