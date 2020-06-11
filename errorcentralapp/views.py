from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from errorcentralapp.filters import ErrorLogFilterSet
from .models import ErrorLog, AppException
from . import serializers
from .serializers import AppExceptionSerializer, ErrorLogSerializerSummary


class ErrorLogListView(mixins.ListModelMixin,
                       GenericViewSet):
    queryset = ErrorLog.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ErrorLogFilterSet
    serializer_class = ErrorLogSerializerSummary

    def get_queryset(self):
        return ErrorLog.objects.values('exception__id', 'exception__title', 'level', 'source', 'environment').annotate(
            events=Count('id')
        )


class ErrorLogView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    queryset = ErrorLog.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ErrorLogFilterSet

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ErrorLogSerializer
        return serializers.ErrorLogSerializerList


class AppExceptionView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       GenericViewSet):
    queryset = AppException.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    serializer_class = AppExceptionSerializer
