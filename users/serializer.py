from rest_framework import serializers
from users.models import User, Payments


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    payment_history = PaymentSerializer(source='payments_set', many=True)

    class Meta:
        model = User
        fields = '__all__'



