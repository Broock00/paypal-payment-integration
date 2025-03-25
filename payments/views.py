# payments/views.py
import paypalrestsdk
import stripe
from square.client import Client
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .models import Payment

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET
})
stripe.api_key = settings.STRIPE_API_KEY
square_client = Client(access_token=settings.SQUARE_ACCESS_TOKEN, environment='sandbox')

class PaymentCreateView(APIView):
    def post(self, request):
        amount = request.data.get('amount')
        method = request.data.get('method')

        if method == 'paypal':
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "transactions": [{"amount": {"total": str(amount), "currency": "USD"}}],
                "redirect_urls": {
                    "return_url": "http://localhost:8000/api/payment/verify/",
                    "cancel_url": "http://localhost:8000/api/payment/cancel/"
                }
            })
            if payment.create():
                Payment.objects.create(
                    user=None,
                    amount=amount,
                    method=method,
                    status='pending',
                    transaction_id=payment.id,
                )
                return Response({"approval_url": payment.links[1].href})
            return Response({"error": "Payment creation failed"}, status=400)

        elif method == 'stripe':
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency='usd',
                payment_method_types=['card']
            )
            return Response({"client_secret": intent['client_secret']})

        elif method == 'square':
            response = square_client.payments.create_payment(body={
                "source_id": request.data.get('nonce'),
                "amount_money": {"amount": int(amount * 100), "currency": "USD"},
                "idempotency_key": str(uuid.uuid4())
            })
            if response.is_success():
                return Response({"transaction_id": response.body['payment']['id']})
            return Response({"error": response.errors}, status=400)

class PaymentVerifyView(APIView):
    def get(self, request):
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            Payment.objects.filter(transaction_id=payment_id).update(
                status='success'
            )
            return Response({"status": "success", "transaction_id": payment.id})
        Payment.objects.filter(transaction_id=payment_id).update(
            status='failed'
        )
        return Response({"status": "failed"}, status=400)