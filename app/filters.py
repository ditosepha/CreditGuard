import django_filters
from .models import Card

class CardFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr="icontains")

    class Meta:
        model = Card
        fields = ['title']