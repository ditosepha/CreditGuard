from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from .models import Card
from .serializers import CardSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .filters import CardFilter
from .permissions import CustomPermission
# Create your views here.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class CardViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [CustomPermission]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CardFilter
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)