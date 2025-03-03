from django.urls import path
from users.apps import UsersConfig
from users.views import ProfilesListAPIView, ProfileRetrieveAPIView, ProfileCreateAPIView, \
    ProfileUpdateAPIView, ProfileDestroyAPIView


app_name = UsersConfig.name


urlpatterns = [
    path('profiles/', ProfilesListAPIView.as_view(), name='profiles'),
    path('profile/<int:pk>/', ProfileRetrieveAPIView.as_view(), name='profile'),
    path('profile/new/', ProfileCreateAPIView.as_view(), name='adding_profile'),
    path('profile/<int:pk>/update/', ProfileUpdateAPIView.as_view(), name='update_profile'),
    path('profile/<int:pk>/delete/', ProfileDestroyAPIView.as_view(), name='delete_profile'),
    ]
