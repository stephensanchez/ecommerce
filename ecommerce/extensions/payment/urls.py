from django.conf.urls import patterns, url, include

from ecommerce.extensions.payment import views
from ecommerce.extensions.order.constants import ORDER_NUMBER_PATTERN
from ecommerce.extensions.payment.constants import CybersourceConstants as CS


CYBERSOURCE_URLS = patterns(
    '',
    url(r'^notify/$', views.CybersourceNotificationView.as_view(), name='notify'),
)

urlpatterns = patterns(
    '',
    url(r'^{cybersource}/'.format(cybersource=CS.NAME), include(CYBERSOURCE_URLS, namespace=CS.NAME)),
    url(r'^receipt/{number}$'.format(number=ORDER_NUMBER_PATTERN), views.ReceiptView.as_view(), name='receipt'),
    url(r'^cancel$', views.CancelView.as_view(), name='cancel'),
)
