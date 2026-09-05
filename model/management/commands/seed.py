from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from model.models import Property


# =====================================================
# DJANGO MANAGEMENT COMMAND
# =====================================================

class Command(BaseCommand):
    help = "Create or update 5 dummy properties"

    def handle(self, *args, **options):

        # =====================================================
        # DUMMY PROPERTY SEED DATA
        # =====================================================

        properties_data = [

            # -------------------------------------------------
            # PROPERTY 01 — LUXURY VILLA
            # -------------------------------------------------
            {
                "title": "Modern Luxury Villa",
                "slug": "modern-luxury-villa",
                "description": (
                    "A beautiful modern luxury villa with spacious rooms, "
                    "premium interiors, natural lighting and a peaceful "
                    "residential environment."
                ),
                "property_type": Property.PropertyType.VILLA,
                "listing_type": Property.ListingType.SALE,
                "status": Property.Status.ACTIVE,
                "price": Decimal("18500000"),
                "bedrooms": 4,
                "bathrooms": Decimal("4.0"),
                "area_sqft": 3200,
                "address": "Green Valley Road",
                "city": "Indore",
                "state": "Madhya Pradesh",
                "country": "India",
                "latitude": Decimal("22.719568"),
                "longitude": Decimal("75.857727"),
                "featured": True,
                "published_at": timezone.now(),
            },

            # -------------------------------------------------
            # PROPERTY 02 — FAMILY HOUSE
            # -------------------------------------------------
            {
                "title": "Elegant Family House",
                "slug": "elegant-family-house",
                "description": (
                    "Comfortable family house located in a peaceful "
                    "neighborhood with modern amenities and excellent "
                    "connectivity."
                ),
                "property_type": Property.PropertyType.HOUSE,
                "listing_type": Property.ListingType.SALE,
                "status": Property.Status.ACTIVE,
                "price": Decimal("9500000"),
                "bedrooms": 3,
                "bathrooms": Decimal("3.0"),
                "area_sqft": 2100,
                "address": "Sunrise Colony",
                "city": "Bhopal",
                "state": "Madhya Pradesh",
                "country": "India",
                "latitude": Decimal("23.259933"),
                "longitude": Decimal("77.412613"),
                "featured": True,
                "published_at": timezone.now(),
            },

            # -------------------------------------------------
            # PROPERTY 03 — CITY APARTMENT
            # -------------------------------------------------
            {
                "title": "Premium City Apartment",
                "slug": "premium-city-apartment",
                "description": (
                    "Premium apartment in the heart of the city featuring "
                    "modern interiors, excellent natural light and convenient "
                    "access to schools, offices and shopping areas."
                ),
                "property_type": Property.PropertyType.APARTMENT,
                "listing_type": Property.ListingType.RENT,
                "status": Property.Status.ACTIVE,
                "price": Decimal("35000"),
                "bedrooms": 2,
                "bathrooms": Decimal("2.0"),
                "area_sqft": 1250,
                "address": "Central Avenue",
                "city": "Pune",
                "state": "Maharashtra",
                "country": "India",
                "latitude": Decimal("18.520430"),
                "longitude": Decimal("73.856744"),
                "featured": False,
                "published_at": timezone.now(),
            },

            # -------------------------------------------------
            # PROPERTY 04 — OFFICE SPACE
            # -------------------------------------------------
            {
                "title": "Contemporary Office Space",
                "slug": "contemporary-office-space",
                "description": (
                    "Professional office space suitable for startups, "
                    "consultants and growing businesses with a modern "
                    "layout and excellent city connectivity."
                ),
                "property_type": Property.PropertyType.OFFICE,
                "listing_type": Property.ListingType.RENT,
                "status": Property.Status.ACTIVE,
                "price": Decimal("65000"),
                "bedrooms": 0,
                "bathrooms": Decimal("2.0"),
                "area_sqft": 1800,
                "address": "Business District",
                "city": "Indore",
                "state": "Madhya Pradesh",
                "country": "India",
                "latitude": Decimal("22.753300"),
                "longitude": Decimal("75.893700"),
                "featured": False,
                "published_at": timezone.now(),
            },

            # -------------------------------------------------
            # PROPERTY 05 — LAND
            # -------------------------------------------------
            {
                "title": "Residential Land Plot",
                "slug": "residential-land-plot",
                "description": (
                    "Well-located residential land plot suitable for "
                    "building a private home or investment property."
                ),
                "property_type": Property.PropertyType.LAND,
                "listing_type": Property.ListingType.SALE,
                "status": Property.Status.ACTIVE,
                "price": Decimal("7200000"),
                "bedrooms": 0,
                "bathrooms": Decimal("0.0"),
                "area_sqft": 2400,
                "address": "New Development Area",
                "city": "Ujjain",
                "state": "Madhya Pradesh",
                "country": "India",
                "latitude": Decimal("23.176466"),
                "longitude": Decimal("75.788513"),
                "featured": False,
                "published_at": timezone.now(),
            },
        ]

        # =====================================================
        # CREATE / UPDATE PROPERTIES
        # =====================================================

        created_count = 0
        updated_count = 0

        for data in properties_data:

            property_obj, created = Property.objects.update_or_create(
                slug=data["slug"],
                defaults=data,
            )

            if created:
                created_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Created: {property_obj.title}"
                    )
                )

            else:
                updated_count += 1

                self.stdout.write(
                    self.style.WARNING(
                        f"↻ Updated: {property_obj.title}"
                    )
                )

        # =====================================================
        # FINAL RESULT
        # =====================================================

        total_count = Property.objects.count()

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "========================================"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "PROPERTY SEED COMPLETED"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "========================================"
            )
        )

        self.stdout.write(
            f"Created : {created_count}"
        )

        self.stdout.write(
            f"Updated : {updated_count}"
        )

        self.stdout.write(
            f"Total   : {total_count}"
        )

        self.stdout.write(
            self.style.SUCCESS(
                "========================================"
            )
        )