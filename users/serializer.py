from rest_framework import serializers
from users.models import User, Payments, SubscriptionForCourse


class PaymentSerializer(serializers.ModelSerializer):
    """Класс сериализатора оплаты пользователя."""

    class Meta:
        """Класс для изменения поведения полей сериализатора модели "Платеж"."""

        model = Payments
        fields = '__all__'


class ProfileUserSerializer(serializers.ModelSerializer):
    """Класс сериализатора пользователя."""

    payment_history = serializers.SerializerMethodField(read_only=True)
    subscriptions = serializers.SerializerMethodField(read_only=True)

    def get_payment_history(self, obj):
        """Метод для вывода информации об истории платежей пользователя."""

        list_payment_history = [
            f'{p.created_at}-({p.payment_amount}, способ оплаты: {p.payment_method}),'
            for p in Payments.objects.filter(owner=obj).order_by("created_at")
        ]
        payment_history = ', '.join(list_payment_history)
        return payment_history

    def get_subscriptions(self, obj):
        """Метод для вывода информации о подписке пользователя на курс."""

        list_subscriptions = [
            f'{s.course}-(pk={s.course.pk}{bool(s.created_at < s.course.updated_at) * "Курс обновлен!"}),'
            for s in SubscriptionForCourse.objects.filter(owner=obj).order_by("created_at")
        ]
        subscriptions = ', '.join(list_subscriptions)
        return subscriptions

    class Meta:
        """Класс для изменения поведения полей сериализатора модели "Пользователь"."""

        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    """Класс сериализатора с ограниченным доступом к модели пользователя."""

    class Meta:
        """Класс для изменения поведения полей сериализатора модели "Пользователь"."""

        model = User
        fields = ['id', 'email', 'avatar', 'phone_number', 'city']


class SubscriptionForCourseSerializer(serializers.ModelSerializer):
    """Класс сериализатора подписки."""

    class Meta:
        """Класс для изменения поведения полей сериализатора модели "Подписка"."""

        model = SubscriptionForCourse
        fields = '__all__'
