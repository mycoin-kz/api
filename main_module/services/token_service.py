"""Service layer for token operations."""

import logging
from typing import List, Optional, Dict, Any

from django.core.cache import cache
from django.db.models import QuerySet, F
from rest_framework.exceptions import ValidationError

from main_module.models import Token
from main_module.serializers import SummaryDataSerializer, FullDataSerializer

logger = logging.getLogger(__name__)


class TokenServiceException(Exception):
    """Base exception for token service."""

    pass


class TokenNotFoundError(TokenServiceException):
    """Raised when a token is not found."""

    pass


class TokenService:
    """Service class for managing cryptocurrency tokens."""

    CACHE_TTL = 300  # 5 minutes
    VALID_SENTIMENTS = {"bullish", "bearish", "neutral"}

    @classmethod
    def _get_cached_data(cls, cache_key: str) -> Optional[Any]:
        """Get data from cache."""
        try:
            return cache.get(cache_key)
        except Exception as e:
            logger.error(f"Cache error for key {cache_key}: {str(e)}")
            return None

    @classmethod
    def _set_cached_data(cls, cache_key: str, data: Any) -> None:
        """Set data in cache."""
        try:
            cache.set(cache_key, data, cls.CACHE_TTL)
        except Exception as e:
            logger.error(f"Failed to cache data for key {cache_key}: {str(e)}")

    @classmethod
    def get_all_tokens(cls) -> List[Dict]:
        """
        Get all available tokens with summary data.

        Returns:
            List of serialized token data

        Raises:
            TokenServiceException: If there's an error fetching tokens
        """
        cache_key = "all_tokens_summary"
        cached_data = cls._get_cached_data(cache_key)

        if cached_data is not None:
            return cached_data

        try:
            tokens = Token.objects.all()
            serializer = SummaryDataSerializer(tokens, many=True)
            data = serializer.data
            cls._set_cached_data(cache_key, data)
            return data
        except Exception as e:
            logger.error(f"Failed to fetch all tokens: {str(e)}")
            raise TokenServiceException("Failed to fetch tokens") from e

    @classmethod
    def get_token_summary(cls, token_id: str) -> Dict:
        """
        Get summary data for a specific token.

        Args:
            token_id: The token's cryptocompare_id

        Returns:
            Serialized token summary data

        Raises:
            TokenNotFoundError: If token is not found
            TokenServiceException: For other errors
        """
        cache_key = f"token_summary_{token_id}"
        cached_data = cls._get_cached_data(cache_key)

        if cached_data is not None:
            return cached_data

        try:
            token = Token.objects.get(cryptocompare_id=token_id)
            serializer = SummaryDataSerializer(token)
            data = serializer.data
            cls._set_cached_data(cache_key, data)
            return data
        except Token.DoesNotExist:
            raise TokenNotFoundError(f"Token {token_id} not found")
        except Exception as e:
            logger.error(f"Error fetching token {token_id}: {str(e)}")
            raise TokenServiceException(f"Failed to fetch token {token_id}") from e

    @classmethod
    def get_token_full_data(cls, token_id: str) -> Dict:
        """
        Get full data for a specific token.

        Args:
            token_id: The token's cryptocompare_id

        Returns:
            Serialized token full data

        Raises:
            TokenNotFoundError: If token is not found
            TokenServiceException: For other errors
        """
        cache_key = f"token_full_{token_id}"
        cached_data = cls._get_cached_data(cache_key)

        if cached_data is not None:
            return cached_data

        try:
            token = Token.objects.get(cryptocompare_id=token_id)
            serializer = FullDataSerializer(token)
            data = serializer.data
            cls._set_cached_data(cache_key, data)
            return data
        except Token.DoesNotExist:
            raise TokenNotFoundError(f"Token {token_id} not found")
        except Exception as e:
            logger.error(f"Error fetching full data for token {token_id}: {str(e)}")
            raise TokenServiceException(
                f"Failed to fetch full data for token {token_id}"
            ) from e

    @classmethod
    def filter_tokens(
        cls,
        min_total_perc: Optional[float] = None,
        sentiment: Optional[str] = None,
    ) -> QuerySet:
        """
        Filter tokens based on criteria.

        Args:
            min_total_perc: Minimum total percentage score
            sentiment: Filter by sentiment (bullish, bearish, neutral)

        Returns:
            QuerySet of filtered tokens

        Raises:
            ValidationError: If invalid parameters are provided
        """
        if sentiment and sentiment not in cls.VALID_SENTIMENTS:
            raise ValidationError(
                f"Invalid sentiment. Must be one of: {cls.VALID_SENTIMENTS}"
            )

        if min_total_perc and (min_total_perc < 0 or min_total_perc > 100):
            raise ValidationError("min_total_perc must be between 0 and 100")

        try:
            tokens = Token.objects.all()

            if min_total_perc is not None:
                tokens = tokens.filter(total_perc__gte=min_total_perc)

            if sentiment:
                if sentiment == "bullish":
                    tokens = tokens.filter(bullish__gt=F("neutral")).filter(
                        bullish__gt=F("bearish")
                    )
                elif sentiment == "bearish":
                    tokens = tokens.filter(bearish__gt=F("neutral")).filter(
                        bearish__gt=F("bullish")
                    )
                elif sentiment == "neutral":
                    tokens = tokens.filter(neutral__gt=F("bullish")).filter(
                        neutral__gt=F("bearish")
                    )

            return tokens
        except Exception as e:
            logger.error(f"Error filtering tokens: {str(e)}")
            raise TokenServiceException("Failed to filter tokens") from e

    @classmethod
    def get_tokens_by_ids(cls, token_ids: list[str]):
        """Fetch multiple tokens by their IDs in a single query."""
        return Token.objects.filter(cryptocompare_id__in=token_ids)
