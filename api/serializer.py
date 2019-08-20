from rest_framework import serializers, generics
from .models import PaymentModel

class PaymentSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField()
    class Meta:
        model = PaymentModel
        fields = '__all__'
        read_only_fields = ['user', 'total', 'last_payment', 'last_payment_date']