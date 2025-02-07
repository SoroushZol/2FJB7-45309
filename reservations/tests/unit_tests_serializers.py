import pytest
from reservations.serializers import TableSerializer, ReservationCreateSerializer, ReservationSerializer
from reservations.models import Table, Reservation
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_table_serializer():
    table = Table.objects.create(seats_count=4, price_per_seat=10.00)
    serializer = TableSerializer(table)
    data = serializer.data
    assert data['seats_count'] == 4
    assert data['price_per_seat'] == 10.00
    assert data['available_seats'] == 4


@pytest.mark.django_db
def test_reservation_create_serializer():
    data = {'seats_count': 3}
    serializer = ReservationCreateSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['seats_count'] == 4  # Rounded up to the next even number


@pytest.mark.django_db
def test_reservation_serializer():
    user = User.objects.create_user(username='testuser', password='testpass')
    table = Table.objects.create(seats_count=4, price_per_seat=10.00)
    reservation = Reservation.objects.create(user=user, table=table, seats_count=2, total_cost=20.00)
    serializer = ReservationSerializer(reservation)
    data = serializer.data
    assert data['user'] == 'testuser'
    assert data['table']['id'] == table.id
    assert data['seats_count'] == 2
    assert data['total_cost'] == 20.00
