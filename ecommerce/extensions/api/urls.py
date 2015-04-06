from django.conf.urls import patterns, url, include

from ecommerce.extensions.api import views
from ecommerce.extensions.order.constants import ORDER_NUMBER_PATTERN


BASKET_URLS = patterns(
    '',
    url(r'^$', views.BasketCreateAPIView.as_view(), name='create'),
)

ORDER_URLS = patterns(
    '',
    # V1 DEPRECATION: Use OrderListAPIView instead of OrderListCreateAPIView. Django stops
    # cascading through URL patterns once it finds one that matches the requested URL, so
    # we can just remove the first of these patterns when we're ready to drop v1.
    url(r'^$', views.OrderListCreateAPIView.as_view(), name='create_list'),
    url(r'^$', views.OrderListAPIView.as_view(), name='list'),
    url(
        r'^{number}/$'.format(number=ORDER_NUMBER_PATTERN),
        views.RetrieveOrderView.as_view(),
        name='retrieve'
    ),
    url(
        r'^{number}/fulfill/$'.format(number=ORDER_NUMBER_PATTERN),
        views.FulfillOrderView.as_view(),
        name='fulfill'
    ),
)

urlpatterns = patterns(
    '',
    url(r'^baskets/', include(BASKET_URLS, namespace='basket')),
    url(r'^orders/', include(ORDER_URLS, namespace='orders')),
)
