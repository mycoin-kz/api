"""Test cases for main module views."""

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta

from main_module.models import Token, Watchlist

User = get_user_model()


@pytest.fixture
def api_client():
    """Create a test API client."""
    return APIClient()


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


@pytest.fixture
def jwt_authenticated_client(api_client, user):
    """Create a JWT authenticated API client."""
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return api_client


@pytest.mark.django_db
class TestViews:
    """Test cases for views."""

    def test_index(self, api_client):
        """Test index endpoint."""
        url = reverse("main_module:index")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "healthy"

    def test_watchlist_unauthorized(self, api_client):
        """Test watchlist endpoint without authentication."""
        url = reverse("main_module:watchlist")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_watchlist(self, jwt_authenticated_client, watchlist_item):
        """Test getting user's watchlist."""
        url = reverse("main_module:watchlist")
        response = jwt_authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["token"] == watchlist_item.token

    def test_add_to_watchlist(self, jwt_authenticated_client, token):
        """Test adding token to watchlist."""
        url = reverse("main_module:watchlist")
        response = jwt_authenticated_client.post(url, {"token": token.cryptocompare_id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["token"] == token.cryptocompare_id

    def test_add_to_watchlist_missing_token(self, jwt_authenticated_client):
        """Test adding to watchlist without token."""
        url = reverse("main_module:watchlist")
        response = jwt_authenticated_client.post(url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_from_watchlist(self, jwt_authenticated_client, watchlist_item):
        """Test deleting from watchlist."""
        url = reverse("main_module:delete_from_watchlist", args=[watchlist_item.token])
        response = jwt_authenticated_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_token_summary(self, jwt_authenticated_client, token):
        """Test getting token summary."""
        url = reverse("main_module:token_summary", args=[token.cryptocompare_id])
        response = jwt_authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["cryptocompare_id"] == token.cryptocompare_id

    def test_token_summary_not_found(self, jwt_authenticated_client):
        """Test getting non-existent token summary."""
        url = reverse("main_module:token_summary", args=["NONEXISTENT"])
        response = jwt_authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_token_full_data(self, jwt_authenticated_client, token):
        """Test getting full token data."""
        url = reverse("main_module:token_full_data", args=[token.cryptocompare_id])
        response = jwt_authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["cryptocompare_id"] == token.cryptocompare_id

    def test_all_tokens(self, jwt_authenticated_client, token):
        """Test getting all tokens."""
        url = reverse("main_module:all_tokens")
        response = jwt_authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["cryptocompare_id"] == token.cryptocompare_id

    def test_filter_tokens(self, jwt_authenticated_client, token):
        """Test filtering tokens."""
        url = reverse("main_module:all_tokens")

        # Test filtering by percentage
        response = jwt_authenticated_client.get(url, {"min_total_perc": 80.0})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        response = jwt_authenticated_client.get(url, {"min_total_perc": 90.0})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

        # Test filtering by sentiment
        response = jwt_authenticated_client.get(url, {"sentiment": "bullish"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        response = jwt_authenticated_client.get(url, {"sentiment": "bearish"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_filter_tokens_invalid_percentage(self, jwt_authenticated_client):
        """Test filtering tokens with invalid percentage."""
        url = reverse("main_module:all_tokens")
        response = jwt_authenticated_client.get(url, {"min_total_perc": "invalid"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_jwt_token_expired(self, api_client, user):
        """Test expired token handling."""
        # Create an expired token by manipulating its payload directly
        token = RefreshToken.for_user(user)
        expired_access_token = token.access_token
        expired_access_token.payload["exp"] = 1  # Set to a timestamp in the past

        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(expired_access_token)}")
        url = reverse("main_module:watchlist")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "token_not_valid" in str(response.content).lower()

    def test_jwt_token_refresh(self, api_client, user):
        """Test token refresh functionality."""
        refresh = RefreshToken.for_user(user)
        url = reverse("auth_module:token_refresh")
        response = api_client.post(url, {"refresh": str(refresh)})
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
