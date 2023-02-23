from rest_framework import serializers
from django.contrib.auth.models import User
from .modelsDjango import *



class ConclusionSerializer(serializers.ModelSerializer):

    class Meta:
        model= Conclusion
        fields=['v1','v2','v3','v4','v5','v6','v7','v8','v9']


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Data
        fields=['latitude','longitude','capture']