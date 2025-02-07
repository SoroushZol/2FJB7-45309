import pytest
from django.contrib.auth.models import User
from reservations.models import Table, Reservation


@pytest.mark.django_db
def test_table_creation():
    table = Table.objects.create(seats_count=4, price_per_seat=10.00)
    assert table.seats_count == 4
    assert table.price_per_seat == 10.00


@pytest.mark.django_db
def test_reservation_creation():
    user = User.objects.create_user(username='testuser', password='testpass')
    table = Table.objects.create(seats_count=4, price_per_seat=10.00)
    reservation = Reservation.objects.create(user=user, table=table, seats_count=2, total_cost=20.00)
    assert reservation.user == user
    assert reservation.table == table
    assert reservation.seats_count == 2
    assert reservation.total_cost == 20.00


@pytest.mark.django_db
def test_table_available_seats():
    table = Table.objects.create(seats_count=4, price_per_seat=10.00, occupied_seats=2)
    assert table.available_seats() == 2


@pytest.mark.django_db
def test_reservation_cancel():
    user = User.objects.create_user(username='testuser', password='testpass')
    table = Table.objects.create(seats_count=4, price_per_seat=10.00, occupied_seats=2)
    reservation = Reservation.objects.create(user=user, table=table, seats_count=2, total_cost=20.00)
    reservation.cancel()
    assert reservation.status == 'Cancelled'
    assert table.occupied_seats == 0
