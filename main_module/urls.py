from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path("watchlist", views.get_watchlist, name="watchlist"),
    path("watchlist/<str:token_id>", views.delete_watchlist, name="delete_watchlist"),
    path("overall_tokens", views.overall_tokens, name="overall_tokens"),
    path("summarydata/<str:token_id>", views.summarydata, name="summarydata"),
    path("signalsdata/<str:token_id>", views.signalsdata, name="signalsdata"),
    path("fulldata/<str:token_id>", views.fulldata, name="fulldata"),
]
