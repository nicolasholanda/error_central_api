from rest_framework import serializers

from .models import ErrorLog, AppException


class AppExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppException
        fields = '__all__'


class ErrorLogSerializerList(serializers.ModelSerializer):
    class Meta:
        model = ErrorLog
        fields = '__all__'


class ErrorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorLog
        fields = ['id', 'description', 'source', 'date', 'level', 'environment', 'exception']
