from rest_framework import serializers
from .models import Refugee, FindRequest, FindResult, Shelter


class ShelterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelter
        fields = '__all__'


class RefugeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refugee
        fields = '__all__'


class ReadRefugeeSerializer(serializers.ModelSerializer):
    shelter = ShelterSerializer()
    class Meta:
        model = Refugee
        fields = '__all__'


class FindResultSerializer(serializers.ModelSerializer):
    refugee = ReadRefugeeSerializer(read_only=True)
    class Meta:
        model = FindResult
        fields = ['refugee', 'percent', 'created', 'modified']

class FindRequestSerializer(serializers.ModelSerializer):
    find_results = FindResultSerializer(many=True, read_only=True)
    class Meta:
        model = FindRequest
        fields = ['contact', 'image', 'status', 'created', 'modified','find_results']
        extra_kwargs = {'status': {'read_only': True}}
