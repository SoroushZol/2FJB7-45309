from rest_framework import serializers
from .models import Table, Seat, Reservation
from django.contrib.auth.models import User


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'table', 'seat_number', 'is_occupied', 'reservation']


class TableSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)  # Nested seats info
    available_seats = serializers.ReadOnlyField()  # Method to show available seats

    class Meta:
        model = Table
        fields = ['id', 'seats_count', 'occupied_seats', 'price_per_seat', 'available_seats', 'seats']


class ReservationSerializer(serializers.ModelSerializer):
    table = TableSerializer(read_only=True)  # Include table details in reservations
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())  # Link to User model
    total_cost = serializers.ReadOnlyField()  # Read-only, calculated in the model

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'table', 'seats_count', 'total_cost', 'status', 'created_at', 'updated_at']

    def validate_seats_count(self, value):
        if value % 2 != 0:
            raise serializers.ValidationError("The number of seats must be an even number.")
        return value

    def create(self, validated_data):
        reservation = super().create(validated_data)
        # Additional actions (like updating the table's occupied seats) can be done here.
        return reservation

    def update(self, instance, validated_data):
        instance.seats_count = validated_data.get('seats_count', instance.seats_count)
        instance.total_cost = instance.seats_count * instance.table.price_per_seat
        instance.save()
        return instance
