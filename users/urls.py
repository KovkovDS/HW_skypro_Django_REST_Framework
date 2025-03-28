from django.urls import path
from rest_framework.permissions import AllowAny
from users.apps import UsersConfig
from users.views import ProfilesListAPIView, ProfileRetrieveAPIView, ProfileCreateAPIView, \
    ProfileUpdateAPIView, ProfileDestroyAPIView, PaymentsListAPIView, PaymentRetrieveAPIView, PaymentCreateAPIView, \
    PaymentUpdateAPIView, PaymentDestroyAPIView, SubscriptionForCourseView, ProfileAdminCreateAPIView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)


app_name = UsersConfig.name

urlpatterns = [
    path('profiles/', ProfilesListAPIView.as_view(), name='profiles'),
    path('profile/<int:pk>/', ProfileRetrieveAPIView.as_view(), name='profile'),
    path('registration/', ProfileCreateAPIView.as_view(), name='registration'),
    path('registration/admin/', ProfileAdminCreateAPIView.as_view(), name='registration_admin'),
    path('profile/<int:pk>/update/', ProfileUpdateAPIView.as_view(), name='update_profile'),
    path('profile/<int:pk>/delete/', ProfileDestroyAPIView.as_view(), name='delete_profile'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments'),
    path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment'),
    path('payment/pay/', PaymentCreateAPIView.as_view(), name='adding_payment'),
    path('payment/<int:pk>/adjust/', PaymentUpdateAPIView.as_view(), name='update_payment'),
    path('payment/<int:pk>/cancel/', PaymentDestroyAPIView.as_view(), name='delete_payment'),
    path('authorization/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='authorization'),
    path('refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('subscription/', SubscriptionForCourseView.as_view(), name='subscription'),
    ]
