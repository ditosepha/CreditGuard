from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import CardViewSet
from rest_framework.authtoken import views

router = DefaultRouter()
router.register(r'cards', CardViewSet, basename='cards')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('token-auth/', views.obtain_auth_token),
]
