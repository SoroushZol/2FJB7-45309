import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from reservations.models import Table, Reservation


@pytest.mark.django_db
def test_list_tables():
    client = APIClient()
    Table.objects.create(seats_count=4, price_per_seat=10.00)
    Table.objects.create(seats_count=6, price_per_seat=15.00)
    url = reverse('tables-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 2


@pytest.mark.django_db
def test_create_reservation():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)
    table = Table.objects.create(seats_count=4, price_per_seat=10.00)
    url = reverse('book-list')
    data = {'seats_count': 4}
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['seats_count'] == 4


@pytest.mark.django_db
def test_cancel_reservation():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)
    table = Table.objects.create(seats_count=4, price_per_seat=10.00, occupied_seats=2)
    reservation = Reservation.objects.create(user=user, table=table, seats_count=2, total_cost=20.00)
    url = reverse('cancel', kwargs={'pk': reservation.id})
    response = client.put(url)
    assert response.status_code == 200
    assert response.data['status'] == 'Reservation cancelled'
