from rest_framework import serializers

from .models import ErrorLog


class ErrorLogSerializerList(serializers.ModelSerializer):
    class Meta:
        model = ErrorLog
        fields = '__all__'


class ErrorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorLog
        fields = ['id', 'description', 'source', 'date', 'level', 'environment']
