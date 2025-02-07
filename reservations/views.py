from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from reservations.filters import TableFilter
from reservations.models import Table, Reservation
from reservations.paginations import TablePagination
from reservations.serializers import TableSerializer, ReservationCreateSerializer, ReservationSerializer


# Create your views here.


class TableViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    # permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated

    # Pagination settings
    pagination_class = TablePagination  # Default pagination is off, but you can enable it if needed.

    # Search filter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TableFilter  # Use the custom filter class
    search_fields = ['id', 'seats_count']
    ordering_fields = ['seats_count', 'price_per_seat']


class ReservationViewSet(ModelViewSet):
    serializer_class = ReservationCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        seats_count = serializer.validated_data['seats_count']
        table = Reservation.find_closest_table(seats_count)
        if table:
            reservation = Reservation.objects.create(
                user=self.request.user,
                table=table,
                seats_count=seats_count,
                status='Booked'
            )
            output_serializer = ReservationSerializer(reservation)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'No available table found for the requested seats count.'},
                        status=status.HTTP_404_NOT_FOUND)
