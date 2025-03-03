from rest_framework import generics
from users.models import User
from users.serializer import ProfileSerializer


class ProfilesListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()


class ProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = ProfileSerializer


class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()


class ProfileDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()

