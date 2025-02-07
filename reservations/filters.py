from django_filters.rest_framework import FilterSet

from reservations.models import Table


class TableFilter(FilterSet):
    class Meta:
        model = Table
        fields = {
            'seats_count': ['gt', 'lt'],
            'occupied_seats': ['gt', 'lt'],
            'price_per_seat': ['gt', 'lt'],
        }

