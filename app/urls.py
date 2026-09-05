from django.urls import path

from . import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Static pages
    path("about/", views.about, name="about"),
    path("terms/", views.terms, name="terms"),
    path("privacy/", views.privacy, name="privacy"),

    # Properties
    path("properties/", views.properties, name="properties"),
    path(
        "properties/<slug:slug>/",
        views.property_detail,
        name="property_detail",
    ),

    # Blog
    path("blog/", views.blog, name="blog"),
    path(
        "blog/<slug:slug>/",
        views.blog_detail,
        name="blog_detail",
    ),

    # Contact
    path("contact/", views.contact, name="contact"),

    # Newsletter
    path(
        "newsletter/subscribe/",
        views.subscribe_newsletter,
        name="subscribe_newsletter",
    ),
]