from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from config.permissions import IsAdminUserCustom
from .models import Listing, ListingImage
from .serializers import (
    ListingSerializer,
    ListingListSerializer,
    ListingImageSerializer,
    ListingImageUploadSerializer,
)
from .filters import ListingFilter
from api.utils.cloudinary import upload_listing_image, delete_image


class ListingListCreateView(generics.ListCreateAPIView):
    """
    GET  /listings/       — public, supports filtering + search + ordering
    POST /listings/       — admin only
    """
    queryset = Listing.objects.prefetch_related("images").all()
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
    queryset = Listing.objects.prefetch_related("images").all()
    serializer_class = ListingSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUserCustom()]


MAX_IMAGES_PER_LISTING = 8


class ListingImageUploadView(APIView):
    """
    POST /listings/<id>/images/
    Upload one or more images for a listing. Admin only.
    Expects multipart/form-data with field: images (accepts multiple files).

    A listing can have at most 8 images total.
    """
    permission_classes = [IsAdminUserCustom]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, id):
        listing = get_object_or_404(Listing, id=id)

        image_files = request.FILES.getlist("images")
        if not image_files:
            return Response(
                {"images": "At least one image file is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_count = listing.images.count()
        slots_remaining = MAX_IMAGES_PER_LISTING - current_count

        if slots_remaining <= 0:
            return Response(
                {"images": f"This listing already has the maximum of {MAX_IMAGES_PER_LISTING} images."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(image_files) > slots_remaining:
            return Response(
                {
                    "images": (
                        f"Only {slots_remaining} image slot(s) remaining. "
                        f"You tried to upload {len(image_files)}."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        created_images = []
        for image_file in image_files:
            serializer = ListingImageUploadSerializer(data={"image": image_file})
            serializer.is_valid(raise_exception=True)

            result = upload_listing_image(serializer.validated_data["image"], str(listing.id))
            listing_image = ListingImage.objects.create(
                listing=listing,
                image_url=result["url"],
                public_id=result["public_id"],
            )
            created_images.append(listing_image)

        return Response(
            ListingImageSerializer(created_images, many=True).data,
            status=status.HTTP_201_CREATED,
        )


class ListingImageDeleteView(APIView):
    """
    DELETE /listings/<id>/images/<image_uid>/
    Remove a specific image from a listing. Admin only.
    Also deletes the asset from Cloudinary.
    """
    permission_classes = [IsAdminUserCustom]

    def delete(self, request, id, image_uid):
        listing = get_object_or_404(Listing, id=id)
        image = get_object_or_404(ListingImage, uid=image_uid, listing=listing)

        # Delete from Cloudinary first, then from DB
        delete_image(image.public_id)
        image.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)