"""Test cases for main module services."""

import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache

from main_module.models import Token, Watchlist
from main_module.services.token_service import TokenService, TokenNotFoundError
from main_module.services.watchlist_service import WatchlistService

User = get_user_model()


@pytest.fixture
def user():
    """Create a test user."""
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def token():
    """Create a test token."""
    return Token.objects.create(
        cryptocompare_id="BTC",
        cryptocompare_symbol="BTC",
        cryptocompare_coinname="Bitcoin",
        cryptocompare_fullname="Bitcoin (BTC)",
        coingecko_id="bitcoin",
        coingecko_symbol="btc",
        coingecko_name="Bitcoin",
        total_perc=85.5,
        bullish=100,
        neutral=50,
        bearish=20,
    )


@pytest.fixture
def watchlist_item(user, token):
    """Create a test watchlist item."""
    return Watchlist.objects.create(user=user, token=token.cryptocompare_id)


@pytest.mark.django_db
class TestWatchlistService:
    """Test cases for WatchlistService."""

    def test_get_user_watchlist(self, user, watchlist_item):
        """Test retrieving user's watchlist."""
        result = WatchlistService.get_user_watchlist(user)
        assert len(result) == 1
        assert result[0]["token"] == watchlist_item.token

    def test_add_to_watchlist(self, user, token):
        """Test adding token to watchlist."""
        result = WatchlistService.add_to_watchlist(user, token.cryptocompare_id)
        assert len(result) == 1
        assert result[0]["token"] == token.cryptocompare_id

    def test_remove_from_watchlist(self, user, watchlist_item):
        """Test removing token from watchlist."""
        result = WatchlistService.remove_from_watchlist(user, watchlist_item.token)
        assert len(result) == 0


@pytest.mark.django_db
class TestTokenService:
    """Test cases for TokenService."""

    def setup_method(self):
        """Clear cache before each test."""
        cache.clear()

    def test_get_all_tokens(self, token):
        """Test retrieving all tokens."""
        result = TokenService.get_all_tokens()
        assert len(result) == 1
        assert result[0]["cryptocompare_id"] == token.cryptocompare_id

    def test_get_token_summary(self, token):
        """Test retrieving token summary."""
        result = TokenService.get_token_summary(token.cryptocompare_id)
        assert result is not None
        assert result["cryptocompare_id"] == token.cryptocompare_id

    def test_get_token_summary_not_found(self):
        """Test retrieving non-existent token."""
        with pytest.raises(TokenNotFoundError) as exc_info:
            TokenService.get_token_summary("NONEXISTENT")
        assert str(exc_info.value) == "Token NONEXISTENT not found"

    def test_get_token_full_data(self, token):
        """Test retrieving full token data."""
        result = TokenService.get_token_full_data(token.cryptocompare_id)
        assert result is not None
        assert result["cryptocompare_id"] == token.cryptocompare_id

    def test_filter_tokens_by_percentage(self, token):
        """Test filtering tokens by percentage."""
        result = TokenService.filter_tokens(min_total_perc=80.0)
        assert len(result) == 1

        result = TokenService.filter_tokens(min_total_perc=90.0)
        assert len(result) == 0

    def test_filter_tokens_by_sentiment(self, token):
        """Test filtering tokens by sentiment."""
        result = TokenService.filter_tokens(sentiment="bullish")
        assert len(result) == 1

        result = TokenService.filter_tokens(sentiment="bearish")
        assert len(result) == 0
