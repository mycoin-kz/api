from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('watchlist/<str:token_id>', views.delete_watchlist, name='delete_watchlist'),
]
