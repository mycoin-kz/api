import logging

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import TokenAuthentication

from main_module.services.watchlist_service import WatchlistService
from main_module.services.token_service import (
    TokenService,
    TokenNotFoundError,
    TokenServiceException,
)
from main_module.serializers import SummaryDataSerializer

logger = logging.getLogger(__name__)


def error_response(
    message: str, status_code: int = status.HTTP_400_BAD_REQUEST
) -> Response:
    """Helper function to create error responses."""
    return Response({"error": message}, status=status_code)


@api_view(["GET"])
def index(request: Request) -> Response:
    """Health check endpoint."""
    return Response({"status": "healthy"})


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def watchlist(request: Request) -> Response:
    """
    Handle watchlist operations.

    GET: Retrieve user's watchlist
    POST: Add a token to watchlist
    """
    try:
        if request.method == "GET":
            data = WatchlistService.get_user_watchlist(request.user)
            return Response(data)

        if request.method == "POST":
            token = request.data.get("token")
            if not token:
                return error_response("Token is required")

            data = WatchlistService.add_to_watchlist(request.user, token)
            return Response(data)
    except Exception as e:
        logger.error(f"Watchlist operation failed: {str(e)}")
        return error_response(
            "Failed to process watchlist operation",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_from_watchlist(request: Request, token_id: str) -> Response:
    """Remove a token from user's watchlist."""
    try:
        data = WatchlistService.remove_from_watchlist(request.user, token_id)
        return Response(data)
    except Exception as e:
        logger.error(f"Failed to delete from watchlist: {str(e)}")
        return error_response(
            "Failed to remove token from watchlist",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def token_summary(request: Request, token_id: str) -> Response:
    """Get summary data for a specific token."""
    try:
        data = TokenService.get_token_summary(token_id)
        return Response(data)
    except TokenNotFoundError:
        return error_response("Token not found", status.HTTP_404_NOT_FOUND)
    except TokenServiceException as e:
        logger.error(f"Token service error: {str(e)}")
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def token_full_data(request: Request, token_id: str) -> Response:
    """Get full data for a specific token."""
    try:
        data = TokenService.get_token_full_data(token_id)
        return Response(data)
    except TokenNotFoundError:
        return error_response("Token not found", status.HTTP_404_NOT_FOUND)
    except TokenServiceException as e:
        logger.error(f"Token service error: {str(e)}")
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_tokens(request: Request) -> Response:
    """Get all available tokens with summary data."""
    try:
        min_total_perc = request.query_params.get("min_total_perc")
        sentiment = request.query_params.get("sentiment")

        if min_total_perc or sentiment:
            try:
                min_total_perc = float(min_total_perc) if min_total_perc else None
            except ValueError:
                return error_response("Invalid min_total_perc value")

            tokens = TokenService.filter_tokens(min_total_perc, sentiment)
            data = SummaryDataSerializer(tokens, many=True).data
            return Response(data)

        data = TokenService.get_all_tokens()
        return Response(data)
    except ValidationError as e:
        return error_response(str(e))
    except TokenServiceException as e:
        logger.error(f"Token service error: {str(e)}")
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
