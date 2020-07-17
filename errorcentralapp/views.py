from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from errorcentralapp.filters import ErrorLogFilterSet
from .models import ErrorLog, AppException, Agent
from . import serializers
from .serializers import AppExceptionSerializer, ErrorLogSerializerSummary, AgentSerializer


class SummaryView(mixins.ListModelMixin,
                  GenericViewSet):
    queryset = ErrorLog.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ErrorLogFilterSet
    ordering_fields = ['events', 'level']
    serializer_class = ErrorLogSerializerSummary

    def get_queryset(self):
        return ErrorLog.objects.values(
            'exception__id',
            'exception__title',
            'level',
            'agent__id',
            'agent__address',
            'environment'
        ).annotate(events=Count('id'))


class ErrorLogView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    queryset = ErrorLog.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['level', 'date', 'environment', 'exception__title']
    filterset_class = ErrorLogFilterSet

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ErrorLogSerializerCreate
        return serializers.ErrorLogSerializerList


class AppExceptionView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       GenericViewSet):
    queryset = AppException.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title']
    serializer_class = AppExceptionSerializer


class AgentView(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                GenericViewSet):
    queryset = Agent.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AgentSerializer
