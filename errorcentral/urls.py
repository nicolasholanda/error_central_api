from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from errorcentralapp import views

router = routers.DefaultRouter()
router.register(r'logs', views.ErrorLogView)
router.register(r'exceptions', views.AppExceptionView)
router.register(r'summaries', views.ErrorLogListView)


urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]
