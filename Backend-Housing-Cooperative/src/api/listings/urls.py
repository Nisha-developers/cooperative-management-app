from django.urls import path
from .views import (
    ListingListCreateView,
    ListingRetrieveUpdateDestroyView,
    ListingImageUploadView,
    ListingImageDeleteView,
)

urlpatterns = [
    path("", ListingListCreateView.as_view(), name="listing-list-create"),
    path("<uuid:id>/", ListingRetrieveUpdateDestroyView.as_view(), name="listing-detail"),
    path("<uuid:id>/images/", ListingImageUploadView.as_view(), name="listing-image-upload"),
    path("<uuid:id>/images/<uuid:image_uid>/", ListingImageDeleteView.as_view(), name="listing-image-delete"),
]