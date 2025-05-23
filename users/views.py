from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from lms.models import Course
from users.models import User, Payments, SubscriptionForCourse
from users.permissions import IsOwner, IsAdministrator, IsUserOwner
from users.serializer import ProfileSerializer, CreateProfileSerializer, PaymentSerializer, ProfileUserSerializer, \
    SubscriptionForCourseSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session, checkout_stripe_session


class ProfilesListAPIView(generics.ListAPIView):
    """Класс представления вида Generic для эндпоинта списка пользователей."""

    serializer_class = ProfileSerializer
    queryset = User.objects.all()


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    """Класс представления вида Generic для эндпоинта просмотра профиля пользователя."""

    serializer_class = ProfileUserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        """Метод получения сериализатора в соответствии с запросом."""

        if self.request.method == 'GET' and self.get_object() != self.request.user or \
                self.request.user.is_superuser is False:
            return ProfileSerializer
        if self.request.user.is_superuser:
            return ProfileUserSerializer
        return ProfileUserSerializer


class ProfileCreateAPIView(generics.CreateAPIView):
    """Класс представления вида Generic для эндпоинта создания пользователя."""

    serializer_class = CreateProfileSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания "Пользователя"."""

        user = serializer.save()
        user.set_password(user.password)
        user.save()


class ProfileAdminCreateAPIView(generics.CreateAPIView):
    """Класс представления вида Generic для эндпоинта создания с административными правами."""

    serializer_class = ProfileUserSerializer
    permission_classes = [IsAuthenticated & IsAdministrator]

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания "Пользователя" с административными правами."""

        user = serializer.save()
        user.groups.add('Администратор')
        user.set_password(user.password)
        user.save()


class ProfileUpdateAPIView(generics.UpdateAPIView):
    """Класс представления вида Generic для эндпоинта редактирования профиля пользователя."""

    serializer_class = ProfileUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated & IsUserOwner | IsAuthenticated & IsAdministrator]


class ProfileDestroyAPIView(generics.DestroyAPIView):
    """Класс представления вида Generic для эндпоинта удаления профиля пользователя."""

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated & IsUserOwner | IsAuthenticated & IsAdministrator]


class PaymentsListAPIView(generics.ListAPIView):
    """Класс представления вида Generic для эндпоинта списка оплат."""

    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('create_at',)
    permission_classes = [IsAuthenticated & IsAdministrator]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Класс представления вида Generic для эндпоинта для просмотра информации об оплате."""

    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated & IsOwner | IsAuthenticated & IsAdministrator]


class PaymentCreateAPIView(generics.CreateAPIView):
    """Класс представления вида Generic для эндпоинта создания оплаты от пользователя."""

    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания "Платежа"."""

        payment = serializer.save(owner=self.request.user)
        stripe_product_id = create_stripe_product(payment)
        stripe_price = create_stripe_price(payment, stripe_product_id)
        session_id, session_url = create_stripe_session(stripe_price)
        payment.session_id = session_id
        payment.payment_link = session_url
        if checkout_stripe_session(payment.session_id):
            payment.save()


class PaymentUpdateAPIView(generics.UpdateAPIView):
    """Класс представления вида Generic для эндпоинта изменения оплаты от пользователя."""

    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated & IsOwner | IsAuthenticated & IsAdministrator]


class PaymentDestroyAPIView(generics.DestroyAPIView):
    """Класс представления вида Generic для эндпоинта удаления оплаты от пользователя."""

    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated & IsAdministrator]


class SubscriptionForCourseView(APIView):
    """Класс представления вида APIView для эндпоинта создания или
    удаления подписки пользователя на курс."""

    queryset = SubscriptionForCourse.objects.all()
    serializer_class = SubscriptionForCourseSerializer
    permission_classes = [IsAuthenticated & IsAdministrator | IsAuthenticated & IsOwner]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['course'],
        properties={
            'course': openapi.Schema(type=openapi.TYPE_INTEGER)
        },
    ))
    def post(self, *args, **kwargs):
        """Метод для отправки запроса на создание или
            удаление подписки пользователя на курс."""

        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = SubscriptionForCourse.objects.all().filter(owner=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена.'
        else:
            SubscriptionForCourse.objects.create(owner=user, course=course_item)
            message = 'Подписка добавлена.'
        return Response({"message": message})
