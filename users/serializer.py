from rest_framework import serializers
from users.models import User, Payments


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'
