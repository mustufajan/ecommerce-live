from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<str:listing_id>", views.listing, name="listing"),
    path("watchlist/<str:listing_id>", views.watchlist, name="watchlist"),
    path("bid/<str:listing_id>", views.bid, name="bid"),
    path("listing_status/<str:listing_id>", views.listing_status, name="listing_status"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("my_bids", views.my_bids, name="my_bids"),
    path("comment/<str:listing_id>", views.comment, name="comment"),
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("categories", views.categories, name="categories"),
    path("categorized_listings/<str:category>", views.categorized_listings, name="categorized_listings")
]
