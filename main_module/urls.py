"""URL configuration for main module."""

from django.urls import path
from . import views

app_name = "main_module"

urlpatterns = [
    path("", views.index, name="index"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path(
        "watchlist/<str:token_id>/",
        views.delete_from_watchlist,
        name="delete_from_watchlist",
    ),
    path("tokens/", views.all_tokens, name="all_tokens"),
    path("tokens/<str:token_id>/summary/", views.token_summary, name="token_summary"),
    path("tokens/<str:token_id>/full/", views.token_full_data, name="token_full_data"),
]
