from rest_framework import serializers
from users.models import User, Payments


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'


class ProfileUserSerializer(serializers.ModelSerializer):
    payment_history = PaymentSerializer(source='payments_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'avatar', 'phone_number', 'city', 'is_active', 'password', 'payment_history']
        # depth = 1


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'avatar', 'phone_number', 'city']
