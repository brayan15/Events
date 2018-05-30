import hashlib
import decimal
from datetime import timedelta
from django.http import Http404
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction
from events.events.models import Event
from django.core.urlresolvers import reverse

# Create your views here.

class TransactionRequestView(LoginRequiredMixin, View):

    template_name = "transactions/complete_transaction.html"

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            event = get_object_or_404 (Event, pk=data['event'])
            transaction = Transaction.objects.create(
                event = event,
                user= request.user,
                value=int(float(data['price']))
            )
        except ValueError:
            messages.error(request, "There is some error in transaction")
            return redirect(reverse("events:detail_event", args=(event.pk)))
        signature = "{}~{}~{}~{}~COP".format(
            settings.PAYU_API_KEY,
            settings.PAYU_MERCHANT_ID,
            transaction.uuid,
            transaction.value)
        md5_signature = hashlib.md5(signature.encode('utf-8'))
        context = {
            'transaction': transaction,
            'payu_url': settings.PAYU_PAYMENT_URL,
            'merchantId': settings.PAYU_MERCHANT_ID,
            'accountId': settings.PAYU_ACCOUNT_ID,
            'signature': md5_signature.hexdigest(),
            'payu_sandbox': 0 if settings.PAYU_PRODUCTION else 1
        }
        return render(request, self.template_name, context)


class ReturnView(LoginRequiredMixin, View):
    template_name = "transactions/payu_return.html"

    def get(self, request, *args, **kwargs):
        try:
            api_key = settings.PAYU_API_KEY
            merchant_id = request.GET['merchantId']
            reference_code = request.GET['referenceCode']
            TX_VALUE = request.GET['TX_VALUE']
            new_value = decimal.Decimal(TX_VALUE)
            new_value = new_value.quantize(
                decimal.Decimal('1.0'),
                decimal.ROUND_HALF_EVEN)
            currency = request.GET['currency']
            transaction_state = request.GET['transactionState']
            sign_string = "{}~{}~{}~{}~{}~{}".format(
                api_key, merchant_id, reference_code,
                new_value, currency, transaction_state)
            createdsign = hashlib.md5(sign_string.encode('utf-8')).hexdigest()
            sign = request.GET['signature']
            reference_pol = request.GET['reference_pol']
            cus = request.GET.get('cus', '')
            extra1 = request.GET['description']
            pse_bank = request.GET.get('pseBank', '')
            lap_payment_method = request.GET['lapPaymentMethod']
            transaction_id = request.GET['transactionId']
            transaction_date = request.GET['processingDate']
            buyer_email = request.GET['buyerEmail']
            payu_message = request.GET.get('message', '')
            context = {
                'cus': cus,
                'pse_bank': pse_bank,
                'currency': currency,
                'description': extra1,
                'total_value': TX_VALUE,
                'buyer_email': buyer_email,
                'payu_message': payu_message,
                'reference_pol': reference_pol,
                'transaction_id': transaction_id,
                'reference_code': reference_code,
                'transaction_date': transaction_date,
                'payment_method': lap_payment_method,
                'transaction_state': transaction_state,
                'valid_transaction': createdsign.upper() == sign.upper(),
            }
            return render(request, self.template_name, context)
        except KeyError:
            raise Http404

class SuccessTransaction(View):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.POST
        merchant_id = data['merchant_id']
        reference_sale = data['reference_sale']
        value = data['value']
        currency = data['currency']
        state_pol = data['state_pol']
        sign = data['sign']
        new_value = decimal.Decimal(value)
        new_value = new_value.quantize(
            decimal.Decimal('1.0'),
            decimal.ROUND_HALF_EVEN)
        sign_string = "{}~{}~{}~{}~{}~{}".format(
            settings.PAYU_API_KEY, merchant_id,
            reference_sale, new_value, currency,
            state_pol)
        createdsign = hashlib.md5(sign_string.encode('utf-8')).hexdigest()
        uuid = data['reference_sale']
        transaction = get_object_or_404(Transaction, uuid=uuid)
    
        if sign.upper() == createdsign.upper():
            if int(state_pol) == 4:
                transaction.success()
                transaction.refresh_from_db()
            else:
                transaction.set_invalid()
            return HttpResponse("Success")
        transaction.set_invalid()
        return HttpResponseForbidden()