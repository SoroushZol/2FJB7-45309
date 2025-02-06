from django.contrib import admin
from .models import Table, Seat, Reservation


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0  # No extra empty rows for seats by default


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'seats_count', 'occupied_seats', 'price_per_seat', 'available_seats')
    list_filter = ('seats_count',)
    search_fields = ('id',)
    inlines = [SeatInline]
    fieldsets = (
        (None, {
            'fields': ('seats_count', 'price_per_seat'),
        }),
        ('Availability', {
            'fields': ('occupied_seats',),
            'classes': ('collapse',)
        }),
    )

    def available_seats(self, obj):
        return obj.available_seats()

    available_seats.short_description = 'Available Seats'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Only populate seats for a new table
            for seat_number in range(1, obj.seats_count + 1):
                Seat.objects.create(table=obj, seat_number=seat_number)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'table', 'seats_count', 'total_cost', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'table__id')
    readonly_fields = ('total_cost', 'created_at', 'updated_at')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('table', 'seat_number', 'is_occupied', 'reservation')
    list_filter = ('is_occupied',)
    search_fields = ('seat_number',)
