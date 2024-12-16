"""Service layer for watchlist operations."""

from typing import List

from django.contrib.auth.models import User as UserType
from django.db.utils import IntegrityError

from main_module.models import Watchlist
from main_module.serializers import WatchlistSerializer


class WatchlistService:
    """Service class for managing user watchlists."""

    @staticmethod
    def get_user_watchlist(user: UserType) -> List[dict]:
        """
        Get the watchlist for a user.

        Args:
            user: The user whose watchlist to retrieve

        Returns:
            List of serialized watchlist items
        """
        serializer = WatchlistSerializer(user.watchlist, many=True)
        return serializer.data

    @staticmethod
    def add_to_watchlist(user: UserType, token: str) -> List[dict]:
        """
        Add a token to user's watchlist.

        Args:
            user: The user to add the token for
            token: The token to add

        Returns:
            Updated list of serialized watchlist items
        """
        try:
            watchlist_obj = Watchlist(user=user, token=token)
            watchlist_obj.save()
        except IntegrityError:
            # Token already exists in watchlist
            pass
        return WatchlistService.get_user_watchlist(user)

    @staticmethod
    def remove_from_watchlist(user: UserType, token_id: str) -> List[dict]:
        """
        Remove a token from user's watchlist.

        Args:
            user: The user to remove the token for
            token_id: The token to remove

        Returns:
            Updated list of serialized watchlist items
        """
        try:
            watchlist = Watchlist.objects.get(user=user, token=token_id)
            watchlist.delete()
        except Watchlist.DoesNotExist:
            pass
        return WatchlistService.get_user_watchlist(user)
