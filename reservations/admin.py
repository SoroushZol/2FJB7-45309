from django.contrib import admin
from .models import Table, Reservation


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'seats_count', 'occupied_seats', 'price_per_seat', 'available_seats')
    list_filter = ('seats_count',)
    search_fields = ('id',)
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


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'table', 'seats_count', 'total_cost', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'table__id')
    readonly_fields = ('total_cost', 'created_at', 'updated_at')
