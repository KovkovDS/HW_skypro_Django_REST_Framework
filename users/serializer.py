from rest_framework import serializers
from users.models import User, Payments, SubscriptionForCourse


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class ProfileUserSerializer(serializers.ModelSerializer):
    payment_history = serializers.SerializerMethodField(read_only=True)
    subscriptions = serializers.SerializerMethodField(read_only=True)

    def get_payment_history(self, obj):
        list_payment_history = [
            f'{p.created_at}-({p.payment_amount}, способ оплаты: {p.payment_method}),'
            for p in Payments.objects.filter(owner=obj).order_by("created_at")
        ]
        payment_history = ', '.join(list_payment_history)
        return payment_history

    def get_subscriptions(self, obj):
        list_subscriptions = [
            f'{s.course}-(pk={s.course.pk}{bool(s.created_at < s.course.updated_at) * "Курс обновлен!"}),'
            for s in SubscriptionForCourse.objects.filter(owner=obj).order_by("created_at")
        ]
        subscriptions = ', '.join(list_subscriptions)
        return subscriptions

    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'avatar', 'phone_number', 'city']


class SubscriptionForCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionForCourse
        fields = '__all__'
