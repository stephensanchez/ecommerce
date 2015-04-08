from django.test import TestCase
from oscar.core.loading import get_model
from oscar.test import factories

from ecommerce.extensions.order.constants import LineStatus as LINE
from ecommerce.extensions.order.processing import EventHandler


ShippingEventType = get_model('order', 'ShippingEventType')
ShippingEvent = get_model('order', 'ShippingEvent')


class EventHandlerTests(TestCase):
    def setUp(self):
        super(EventHandlerTests, self).setUp()
        self.shipping_event_type = ShippingEventType.objects.create(code='shipped', name='shipped')
        self.order = factories.create_order()

    def test_create_shipping_event_all_lines_complete(self):
        """
        ShippingEvents should only be created if at least one line item in an order has been successfully fulfilled. The
        created ShippingEvent should only contain the fulfilled line items. If no line items have been fulfilled, no
        ShippingEvent should be created.
        """
        order = self.order
        self.assertEqual(order.lines.count(), 1)
        line = order.lines.first()
        line.status = LINE.COMPLETE
        line.save()

        self.assertEqual(order.shipping_events.count(), 0)
        EventHandler().create_shipping_event(order, self.shipping_event_type, order.lines.all(), [1])

        shipping_event = order.shipping_events.first()
        self.assertEqual(shipping_event.order.id, order.id)
        self.assertEqual(shipping_event.lines.count(), 1)
        self.assertEqual(shipping_event.lines.first().id, line.id)

    def test_create_shipping_event_all_lines_failed(self):
        """ If no line items have been fulfilled, no ShippingEvent should be created. """
        order = self.order
        self.assertEqual(order.lines.count(), 1)
        line = order.lines.first()
        line.status = LINE.FULFILLMENT_CONFIGURATION_ERROR
        line.save()

        self.assertEqual(order.shipping_events.count(), 0)
        EventHandler().create_shipping_event(order, self.shipping_event_type, order.lines.all(), [1])
        self.assertEqual(order.shipping_events.count(), 0,
                         'No ShippingEvent should have been created for an order with no fulfilled line items.')

    def test_create_shipping_event_mixed_line_status(self):
        """ The created ShippingEvent should only contain the fulfilled line items. """
        # Create a basket with multiple items
        basket = factories.create_basket()
        product = factories.create_product()
        factories.create_stockrecord(product, num_in_stock=2)
        basket.add_product(product)

        # Create an order from the basket and verify a line item exists for each item in the basket
        order = factories.create_order(basket=basket)
        self.assertEqual(order.lines.count(), 2)
        statuses = (LINE.COMPLETE, LINE.FULFILLMENT_CONFIGURATION_ERROR,)

        lines = order.lines.all()
        for index, line in enumerate(lines):
            line.status = statuses[index]
            line.save()

        self.assertEqual(order.shipping_events.count(), 0)
        EventHandler().create_shipping_event(order, self.shipping_event_type, lines, [1, 1])

        # Verify a single shipping event was created and that the event only contains the complete line item
        self.assertEqual(order.shipping_events.count(), 1)
        shipping_event = order.shipping_events.first()
        self.assertEqual(shipping_event.order.id, order.id)
        self.assertEqual(shipping_event.lines.count(), 1)
        self.assertEqual(shipping_event.lines.first().id, lines[0].id)

        # Fulfill all line items and create a new shipping event
        lines.update(status=LINE.COMPLETE)
        EventHandler().create_shipping_event(order, self.shipping_event_type, lines, [1, 1])

        # Verify a second shipping event was created for the newly-fulfilled line item
        self.assertEqual(order.shipping_events.count(), 2)
        shipping_event = order.shipping_events.all()[0]
        self.assertEqual(shipping_event.order.id, order.id)
        self.assertEqual(shipping_event.lines.count(), 1)
        self.assertEqual(shipping_event.lines.first().id, lines[1].id)
