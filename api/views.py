from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import PaymentModel
from .serializer import PaymentSerializer
from paystack.resource import TransactionResource
from rest_framework.response import Response
from rest_framework import status
import random
import string
from datetime import datetime
from django.conf import settings


# Create your views here.

class HomePageView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PaymentSerializer
    queryset = PaymentModel.objects.all()

    def get(self, request, *args, **kwargs):
        query = PaymentModel.objects.get(user = request.user.get_username())
        resp = {
            'User': self.request.user.get_username(),
            'Date and Time': datetime.now().strftime('%Y-%m-%d %T'),
            'Total': query.total
        }

        return Response(resp, status=status.HTTP_200_OK)


class PaymentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = PaymentModel.objects.all()
    serializer_class = PaymentSerializer
    rand = ''.join(
        [random.choice(
            string.ascii_letters + string.digits) for n in range(16)])

    def perform_create(self, serializer):
        serializer.save(
            user = self.request.user.get_username(),
            total = 10000,
        )
    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data = self.request.data,
                                         context={'request': request})
        self.serializer.is_valid(raise_exception = True)

        secret_key = settings.PAYSTACK_SECRET_KEY
        random_ref = self.rand
        email = request.user.email
        amount = self.serializer.data.get('amount')
        try:
            client = TransactionResource(secret_key, random_ref)
            response = client.initialize(amount*100,
                                         email)
            client.authorize()
            if PaymentModel.objects.filter(user = request.user.get_username()).exists():
                to_up = PaymentModel.objects.get(user = request.user.get_username())
                to_up.total = to_up.total + amount
                to_up.last_payment = amount
                to_up.last_payment_date = datetime.now().strftime('%Y-%m-%d %T')
                to_up.save()
            else:
                PaymentModel.objects.create(
                    user = request.user.get_username(),
                    total = amount,
                    last_payment = amount,
                    last_payment_date = datetime.now().strftime('%Y_%m_%d %T')
                    )
                to_up = amount
            resp = {
                'Ref': random_ref,
                'User': self.request.user.get_username(),
                'Email': email,
                'Date and Time': datetime.now().strftime('%Y_%m_%d %T'),
                'Amount Paid': '# {}'.format(amount),
                'Total': to_up.total,
            }
            return Response(resp, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Invalid Transaction!'}, status=status.HTTP_400_BAD_REQUEST)



