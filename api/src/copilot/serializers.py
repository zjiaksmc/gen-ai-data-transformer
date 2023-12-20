from rest_framework import serializers
from .models import *

class ChatSessionSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=128)
    session_name = serializers.CharField(max_length=50)
    created_dt = serializers.DateTimeField()
    user_id = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=50)
    is_active = serializers.IntegerField()