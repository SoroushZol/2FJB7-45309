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


class Seat(models.Model):
    table = models.ForeignKey(Table, related_name='seats', on_delete=models.CASCADE)
    seat_number = models.IntegerField()  # Seat number in the table
    is_occupied = models.BooleanField(default=False)  # Whether this seat is occupied or not
    reservation = models.ForeignKey('Reservation', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Seat {self.seat_number} at Table {self.table.id}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who made the reservations
    table = models.ForeignKey(Table, related_name='reservations', on_delete=models.CASCADE)  # Reserved table
    seats_count = models.IntegerField()  # Number of seats reserved (rounded to even number)
    total_cost = models.DecimalField(max_digits=6, decimal_places=2)  # Total reservations cost
    status = models.CharField(max_length=20, choices=[('Booked', 'Booked'), ('Cancelled', 'Cancelled')],
                              default='Booked')
    created_at = models.DateTimeField(auto_now_add=True)  # When the reservations was made
    updated_at = models.DateTimeField(auto_now=True)  # Last update to the reservations

    def save(self, *args, **kwargs):
        # Round seats_count to the next even number if odd
        if self.seats_count % 2 != 0:
            self.seats_count += 1
        # Calculate total cost based on the number of seats reserved
        self.total_cost = self.seats_count * self.table.price_per_seat
        # Update table's occupied_seats
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
