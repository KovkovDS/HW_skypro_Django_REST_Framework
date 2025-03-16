from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from lms.models import Course
from users.models import User, Payments, SubscriptionForCourse
from users.permissions import IsOwner, IsAdministrator, IsUserOwner
from users.serializer import ProfileSerializer, PaymentSerializer, ProfileUserSerializer, \
    SubscriptionForCourseSerializer


class ProfilesListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileUserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.get_object() != self.request.user or self.request.user.is_superuser is False:
            return ProfileSerializer
        if self.request.user.is_superuser:
            return ProfileUserSerializer
        return ProfileUserSerializer


class ProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = ProfileUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProfileUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated & IsUserOwner | IsAuthenticated & IsAdministrator]


class ProfileDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated & IsUserOwner | IsAuthenticated & IsAdministrator]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('create_at',)
    permission_classes = [IsAuthenticated & IsAdministrator]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated & IsOwner | IsAuthenticated & IsAdministrator]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer


class PaymentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated & IsOwner | IsAuthenticated & IsAdministrator]


class PaymentDestroyAPIView(generics.DestroyAPIView):
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated & IsAdministrator]


class SubscriptionForCourseView(APIView):
    queryset = SubscriptionForCourse.objects.all()
    serializer_class = SubscriptionForCourseSerializer
    permission_classes = [IsAuthenticated & IsAdministrator | IsAuthenticated & IsOwner]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = SubscriptionForCourse.objects.all().filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            SubscriptionForCourse.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'
        return Response({"message": message})
