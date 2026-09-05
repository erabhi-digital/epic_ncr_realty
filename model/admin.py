from django.contrib import admin
from .models import (
    Agent,
    Amenity,
    BlogPost,
    ContactInquiry,
    NewsletterSubscriber,
    Property,
    PropertyAmenity,
    PropertyImage,
)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 0
    fields = ("image", "alt_text", "is_primary", "sort_order")
    ordering = ("sort_order", "id")


class PropertyAmenityInline(admin.TabularInline):
    model = PropertyAmenity
    extra = 0
    autocomplete_fields = ("amenity",)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title", "property_type", "listing_type", "price",
        "city", "status", "featured", "agent", "published_at",
    )
    list_filter = ("status", "property_type", "listing_type", "featured", "city")
    search_fields = ("title", "address", "city", "state", "agent__name")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("agent",)
    list_select_related = ("agent",)
    list_per_page = 50
    date_hierarchy = "published_at"
    inlines = (PropertyImageInline, PropertyAmenityInline)

    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "slug", "description", "property_type", "listing_type", "status")
        }),
        ("Pricing & Size", {
            "fields": ("price", "bedrooms", "bathrooms", "area_sqft")
        }),
        ("Location", {
            "fields": ("address", "city", "state", "country", "latitude", "longitude")
        }),
        ("Publishing", {
            "fields": ("featured", "published_at", "agent")
        }),
    )


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ("property", "is_primary", "sort_order", "created_at")
    list_filter = ("is_primary",)
    search_fields = ("property__title", "alt_text")
    autocomplete_fields = ("property",)
    list_select_related = ("property",)
    list_per_page = 50


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "email", "phone", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "email", "phone")
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 50


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")
    search_fields = ("name",)
    list_per_page = 50


@admin.register(PropertyAmenity)
class PropertyAmenityAdmin(admin.ModelAdmin):
    list_display = ("property", "amenity")
    search_fields = ("property__title", "amenity__name")
    autocomplete_fields = ("property", "amenity")
    list_select_related = ("property", "amenity")
    list_per_page = 50


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "published_at", "created_at")
    list_filter = ("is_published", "published_at")
    search_fields = ("title", "excerpt", "content", "author__name")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("author",)
    list_select_related = ("author",)
    list_per_page = 50
    date_hierarchy = "published_at"


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "property", "is_resolved", "created_at")
    list_filter = ("is_resolved", "created_at")
    search_fields = ("name", "email", "phone", "subject", "message")
    autocomplete_fields = ("property",)
    list_select_related = ("property",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 50


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("email",)
    list_per_page = 100


admin.site.site_header = "ModernEstate Administration"
admin.site.site_title = "ModernEstate Admin"
admin.site.index_title = "Real Estate Management"
