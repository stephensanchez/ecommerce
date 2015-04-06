"""Ecommerce API constants."""


class EcommerceAPIDictionaryKeys(object):
    """Dictionary keys used repeatedly in the ecommerce API."""
    ORDER = u'order'
    ORDER_NUMBER = u'number'
    SHIPPING_METHOD = u'shipping_method'
    SHIPPING_CHARGE = u'shipping_charge'
    ORDER_TOTAL = u'total'
    PAYMENT_PARAMETERS = u'payment_parameters'


class EcommerceAPIConstants(object):
    """Constants used throughout the ecommerce API."""
    KEYS = EcommerceAPIDictionaryKeys()
