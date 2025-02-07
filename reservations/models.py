from django.db import models
from django.contrib.auth.models import User


class Table(models.Model):
    SEAT_CHOICES = [
        (i, f"{i} seats") for i in range(4, 11, 2)  # Support tables with 4 to 10 seats
    ]

    id = models.AutoField(primary_key=True)
    seats_count = models.IntegerField(choices=SEAT_CHOICES)  # M seats (between 4 and 10)
    occupied_seats = models.IntegerField(default=0)  # Number of seats already reserved
    price_per_seat = models.DecimalField(max_digits=6, decimal_places=2)  # Price for each seat (X)

    def available_seats(self):
        return self.seats_count - self.occupied_seats  # Calculates remaining available seats

    def __str__(self):
        return f"Table {self.id} ({self.seats_count} seats)"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, related_name='reservations', on_delete=models.CASCADE)
    seats_count = models.IntegerField()
    total_cost = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Booked', 'Booked'), ('Cancelled', 'Cancelled')],
                              default='Booked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Round seats_count to the next even number if odd
        self.total_cost = (self.table.seats_count - 1) * self.table.price_per_seat
        self.table.occupied_seats += self.seats_count
        self.table.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation for {self.user.username} at Table {self.table.id} ({self.seats_count} seats)"

    def cancel(self):
        self.status = 'Cancelled'
        self.table.occupied_seats -= self.seats_count  # Free up the seats
        self.table.save()
        self.save()

    @staticmethod
    def find_closest_table(seats_count):
        tables = Table.objects.filter(
            seats_count__gte=seats_count,
            occupied_seats__lt=models.F('seats_count')
            ).order_by('seats_count')
        return tables.first() if tables else None
