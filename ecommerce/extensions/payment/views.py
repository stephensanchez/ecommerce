"""Views for interacting with payment processors."""
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from oscar.core.loading import get_model
from oscar.apps.checkout.mixins import OrderPlacementMixin
from oscar.apps.payment.models import SourceType

from ecommerce.extensions.order.models import Order
from ecommerce.extensions.fulfillment.status import ORDER
from ecommerce.extensions.fulfillment.mixins import FulfillmentMixin
from ecommerce.extensions.payment.processors import Cybersource
from ecommerce.extensions.payment.constants import ProcessorConstants as PC
from ecommerce.extensions.payment.helpers import get_processor_class


SourceType = get_model('payment', 'SourceType')
Order = get_model('order', 'Order')


class CybersourceNotificationView(View, OrderPlacementMixin, FulfillmentMixin):
    """Handle a "merchant notification" from CyberSource.

    CyberSource will notify this endpoint after a transaction completes with information
    about the transaction. If the transaction completed successfully and the parameters
    received are signed correctly, the order associated with the transaction is fulfilled.
    """
    def post(self, request):
        """Parse and verify the integrity of received transaction data.

        If the data does not appear to have been tampered with and the transaction was
        successfully processed, fulfills the order corresponding to the "reference number"
        contained in the received data.

        Returns:
            HTTP_200_OK
        """
        transaction_data = request.POST.dict()
        # TODO: Pick up here! Use built in payment processing.
        result = Cybersource().handle_processor_response(transaction_data)

        if result[PC.SUCCESS]:
            # get the order
            order = Order.objects.get(number=result[PC.ORDER_NUMBER])
            # register the money in Oscar
            self._register_payment(order, self.Cybersource.NAME)
            # fulfill the order
            self._fulfill_order(order)

        return HttpResponse()

    def _register_payment(self, order, processor_name):
        """
        Records the payment source and event and updates the order status

        Args:
            order (Order): the order that is being paid for
            processor_name (str): the name of the processor that will be processing this payment

        Returns:
            None
        """

        # get the source
        source_type, _ = SourceType.objects.get_or_create(name=processor_name)
        source = source_type.sources.model(
            source_type=source_type, amount_allocated=order.total_excl_tax, currency=order.currency
        )

        # record payment events
        self.add_payment_source(source)
        self.add_payment_event(PC.PAID_EVENT_NAME, order.total_excl_tax, order.number)
        self.save_payment_details(order)

        # update the status of the order
        order.set_status(ORDER.PAID)


class ReceiptView(View):
    """Display a receipt page corresponding to a successful transaction.

    Users can be redirected to this view after successfully completing a transaction.
    """
    def get(self, request, number):
        pass


class CancelView(View):
    """Display a transaction cancellation page.

    Users can be redirected to this view after choosing to cancel a transaction.
    """
    def get(self, request):
        pass
