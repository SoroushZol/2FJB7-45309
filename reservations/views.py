from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
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


class ReservationViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = ReservationCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    @swagger_auto_schema(operation_description="List all reservations")
    def list(self, request, *args, **kwargs):
        """
        list all reservations
        """
        queryset = self.get_queryset()
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Book some seats")
    def create(self, request, *args, **kwargs):
        """
        book some seats
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        seats_count = serializer.validated_data['seats_count']
        table = Reservation.find_closest_table(seats_count)
        if table:
            if table.seats_count == seats_count:
                total_cost = (table.seats_count - 1) * table.price_per_seat
            else:
                total_cost = seats_count * table.price_per_seat

            reservation = Reservation.objects.create(
                user=self.request.user,
                table=table,
                total_cost=total_cost,
                seats_count=seats_count,
                status='Booked'
            )
            table.occupied_seats += seats_count
            table.save()

            output_serializer = ReservationSerializer(reservation)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'No available table found for the requested seats count.'},
                        status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(operation_description="Cancel a reservation")
    def update(self, request, *args, **kwargs):
        """
        Cancel a reservation with specific id
        """
        reservation = self.get_object()
        if reservation.status == 'Booked':
            reservation.cancel()
            return Response({'status': 'Reservation cancelled'}, status=status.HTTP_200_OK)
        return Response({'error': 'Reservation cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)
