"""Throttles for rate-limiting requests to API endpoints."""
from django.conf import settings
from rest_framework.throttling import UserRateThrottle


class BasketsThrottle(UserRateThrottle):
    """Limit the number of requests users can make to basket-related endpoints."""
    rate = settings.RATE_LIMITS.get('BASKET_ENDPOINTS', '40/minute')


class OrdersThrottle(UserRateThrottle):
    """Limit the number of requests users can make to order-related endpoints."""
    rate = settings.RATE_LIMITS.get('ORDER_ENDPOINTS', '40/minute')
