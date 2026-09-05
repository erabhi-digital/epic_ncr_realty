import logging

from django.contrib import messages
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import DatabaseError, transaction
from django.db.models import Prefetch, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods

from model.models import (
    Agent,
    BlogPost,
    ContactInquiry,
    NewsletterSubscriber,
    Property,
    PropertyImage,
)

logger = logging.getLogger(__name__)

PROPERTY_IMAGE_QS = PropertyImage.objects.only(
    "id", "property_id", "image", "alt_text", "is_primary", "sort_order"
).order_by("sort_order", "id")


def _published_properties():
    """Base queryset used by property pages; avoids N+1 queries."""
    return (
        Property.objects
        .filter(status=Property.Status.ACTIVE)
        .select_related("agent")
        .prefetch_related(
            Prefetch("images", queryset=PROPERTY_IMAGE_QS, to_attr="cached_images")
        )
    )


@cache_page(60 * 5)
def home(request):
    try:
        featured = list(
            _published_properties()
            .filter(featured=True)
            .only(
                "id", "title", "slug", "price", "city", "property_type",
                "listing_type", "bedrooms", "bathrooms", "area_sqft",
                "featured", "agent_id",
            )[:6]
        )

        # Fallback keeps the home page populated if fewer than 6 properties
        # are marked featured.
        if len(featured) < 6:
            extra = (
                _published_properties()
                .filter(featured=False)
                .only(
                    "id", "title", "slug", "price", "city", "property_type",
                    "listing_type", "bedrooms", "bathrooms", "area_sqft",
                    "featured", "agent_id",
                )
                .exclude(pk__in=[p.pk for p in featured])[:6 - len(featured)]
            )
            featured.extend(extra)

        latest_posts = (
            BlogPost.objects
            .filter(is_published=True)
            .select_related("author")
            .only("id", "title", "slug", "excerpt", "cover_image", "published_at", "author_id")
            [:3]
        )

        return render(request, "pages/home.html", {
            "featured_properties": featured,
            "latest_posts": latest_posts,
        })
    except DatabaseError:
        logger.exception("Database error while loading home page")
        return render(request, "errors/500.html", status=500)


@cache_page(60 * 10)
def about(request):
    agents = Agent.objects.filter(is_active=True).only(
        "id", "name", "slug", "role", "photo", "bio", "email", "phone"
    )[:8]
    return render(request, "pages/about.html", {"agents": agents})


def properties(request):
    try:
        qs = _published_properties().only(
            "id", "title", "slug", "price", "city", "state", "property_type",
            "listing_type", "bedrooms", "bathrooms", "area_sqft",
            "featured", "published_at", "agent_id",
        )

        # GET filters are intentionally whitelist-based.
        location = request.GET.get("location", "").strip()
        property_type = request.GET.get("property_type", "").strip()
        listing_type = request.GET.get("listing_type", "").strip()
        min_price = request.GET.get("min_price", "").strip()
        max_price = request.GET.get("max_price", "").strip()
        bedrooms = request.GET.get("bedrooms", "").strip()
        sort = request.GET.get("sort", "newest").strip()

        if location:
            qs = qs.filter(
                Q(city__icontains=location) |
                Q(state__icontains=location) |
                Q(address__icontains=location)
            )

        valid_types = {v for v, _ in Property.PropertyType.choices}
        valid_listing = {v for v, _ in Property.ListingType.choices}

        if property_type in valid_types:
            qs = qs.filter(property_type=property_type)

        if listing_type in valid_listing:
            qs = qs.filter(listing_type=listing_type)

        try:
            if min_price:
                qs = qs.filter(price__gte=max(0, float(min_price)))
            if max_price:
                qs = qs.filter(price__lte=max(0, float(max_price)))
            if bedrooms.isdigit():
                qs = qs.filter(bedrooms__gte=int(bedrooms))
        except (TypeError, ValueError, OverflowError):
            messages.warning(request, "Some price/bedroom filters were ignored.")

        ordering = {
            "newest": "-published_at",
            "price_low": "price",
            "price_high": "-price",
        }.get(sort, "-published_at")
        qs = qs.order_by(ordering, "-id")

        paginator = Paginator(qs, 12)
        page_obj = paginator.get_page(request.GET.get("page"))

        return render(request, "pages/properties.html", {
            "page_obj": page_obj,
            "properties": page_obj.object_list,
            "filters": request.GET,
        })
    except DatabaseError:
        logger.exception("Database error while loading property listing")
        return render(request, "errors/500.html", status=500)


def property_detail(request, slug):
    try:
        property_obj = get_object_or_404(
            _published_properties()
            .only(
                "id", "title", "slug", "description", "property_type",
                "listing_type", "status", "price", "bedrooms", "bathrooms",
                "area_sqft", "address", "city", "state", "country",
                "latitude", "longitude", "featured", "published_at", "agent_id",
            ),
            slug=slug,
        )
        return render(request, "pages/property_detail.html", {
            "property": property_obj,
            "images": property_obj.cached_images,
        })
    except DatabaseError:
        logger.exception("Database error for property slug=%s", slug)
        return render(request, "errors/500.html", status=500)


@cache_page(60 * 5)
def blog(request):
    posts = (
        BlogPost.objects
        .filter(is_published=True)
        .select_related("author")
        .only(
            "id", "title", "slug", "excerpt", "cover_image",
            "published_at", "author_id", "author__name",
        )
    )
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "pages/blog.html", {
        "page_obj": page_obj,
        "posts": page_obj.object_list,
    })


def blog_detail(request, slug):
    post = get_object_or_404(
        BlogPost.objects.select_related("author").only(
            "id", "title", "slug", "excerpt", "content", "cover_image",
            "published_at", "author_id", "author__name",
        ),
        slug=slug,
        is_published=True,
    )
    return render(request, "pages/blog_detail.html", {"post": post})


@require_http_methods(["GET", "POST"])
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()
        property_id = request.POST.get("property_id", "").strip()

        if not name or not email or not subject or not message:
            messages.error(request, "Please fill in all required fields.")
            return render(request, "pages/contact.html", status=400)

        try:
            with transaction.atomic():
                inquiry = ContactInquiry.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    subject=subject,
                    message=message,
                    property_id=int(property_id) if property_id.isdigit() else None,
                )

            logger.info("Created contact inquiry id=%s", inquiry.pk)
            messages.success(request, "Thanks. Your message has been sent.")
            return redirect("contact")
        except (DatabaseError, ValueError):
            logger.exception("Failed to create contact inquiry")
            messages.error(request, "We could not send your message. Please try again.")
            return render(request, "pages/contact.html", status=500)

    return render(request, "pages/contact.html")


@require_http_methods(["POST"])
def subscribe_newsletter(request):
    email = request.POST.get("email", "").strip().lower()

    if not email:
        messages.error(request, "Please enter a valid email address.")
        return redirect(request.META.get("HTTP_REFERER", "home"))

    try:
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={"is_active": True},
        )
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save(update_fields=["is_active", "updated_at"])

        messages.success(request, "You are subscribed to the newsletter.")
    except DatabaseError:
        logger.exception("Newsletter subscription failed")
        messages.error(request, "Subscription failed. Please try again.")

    return redirect(request.META.get("HTTP_REFERER", "home"))




def terms(request):
    return render(request, "pages/terms.html")


def privacy(request):
    return render(request, "pages/privacy.html")
