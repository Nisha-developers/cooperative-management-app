from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from config.permissions import IsAdminUserCustom
from .models import Listing
from .serializers import ListingSerializer, ListingListSerializer
from .filters import ListingFilter


class ListingListCreateView(generics.ListCreateAPIView):
    """
    GET  /listings/       — public, supports filtering + search + ordering
    POST /listings/       — admin only
    """
    queryset = Listing.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = ListingFilter
    search_fields = ["title", "address", "city", "state", "description"]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUserCustom()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ListingListSerializer
        return ListingSerializer


class ListingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /listings/<id>/   — public
    PATCH  /listings/<id>/   — admin only
    DELETE /listings/<id>/   — admin only
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUserCustom()]