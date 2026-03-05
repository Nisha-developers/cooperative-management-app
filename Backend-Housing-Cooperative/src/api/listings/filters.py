import django_filters
from .models import Listing, ListingType, PropertyType, ListingStatus


class ListingFilter(django_filters.FilterSet):
    listing_type = django_filters.ChoiceFilter(choices=ListingType.choices)
    property_type = django_filters.ChoiceFilter(choices=PropertyType.choices)
    status = django_filters.ChoiceFilter(choices=ListingStatus.choices)
    allows_installment = django_filters.BooleanFilter()

    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    min_bedrooms = django_filters.NumberFilter(field_name="bedrooms", lookup_expr="gte")

    state = django_filters.CharFilter(lookup_expr="iexact")
    city = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Listing
        fields = [
            "listing_type",
            "property_type",
            "status",
            "allows_installment",
            "min_price",
            "max_price",
            "min_bedrooms",
            "state",
            "city",
        ]