from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reservations.views import TableViewSet, ReservationViewSet

router = DefaultRouter()
router.register('tables', TableViewSet, basename='tables')
router.register('book', ReservationViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]
