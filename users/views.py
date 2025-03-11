from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User, Payments
from users.permissions import IsOwner, IsAdministrator
from users.serializer import ProfileSerializer, PaymentSerializer, ProfileUserSerializer


class ProfilesListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileUserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        if self.request.user == user or self.request.user.get_user_permissions('IsAdministrator'):
            serializer_class = ProfileUserSerializer(user)
        else:
            serializer_class = ProfileSerializer(user)
        return serializer_class


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
    permission_classes = [IsAuthenticated & IsOwner | IsAdministrator]


class ProfileDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated & IsOwner | IsAdministrator]


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
