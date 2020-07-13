from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import ErrorLog, AppException


class AppExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppException
        fields = '__all__'


class AppExceptionSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = AppException
        fields = ['title']
        extra_kwargs = {
            'id': {'read_only': False},
            'title': {'validators': []}
        }


class ErrorLogSerializerSummary(serializers.ModelSerializer):
    events = serializers.IntegerField()
    exception = AppExceptionSerializer()

    class Meta:
        model = ErrorLog
        fields = ['level', 'agent', 'environment', 'exception', 'events']

    def to_representation(self, instance):
        exception = AppException(id=instance.pop('exception__id'),
                                 title=instance.pop('exception__title'))
        instance['exception'] = exception
        return super().to_representation(instance)


class ErrorLogSerializerList(serializers.ModelSerializer):
    class Meta:
        model = ErrorLog
        fields = '__all__'


class ErrorLogSerializer(serializers.ModelSerializer):
    exception = AppExceptionSerializerCreate()

    class Meta:
        model = ErrorLog
        fields = ['id', 'description', 'agent', 'date', 'level', 'environment', 'exception']

    def create(self, validated_data):
        exception_title = validated_data.pop('exception')['title']
        try:
            exception = AppException.objects.filter(title__iexact=exception_title).get()
        except ObjectDoesNotExist:
            exception = AppException.objects.create(title=exception_title)
        validated_data['exception'] = exception
        return ErrorLog.objects.create(**validated_data)
