from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from lms.models import Course, Lesson
from lms.paginators import LessonsPaginator, CoursesPaginator
from lms.serializer import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursesPaginator

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated & ~IsModerator]
        elif self.action in ['list', 'change', 'retrieve']:
            self.permission_classes = [IsAuthenticated & IsModerator | IsAuthenticated & IsOwner]
        elif self.action in ['destroy']:
            self.permission_classes = [IsAuthenticated & IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

    def get_queryset(self):

        if self.permission_classes != (IsModerator | IsOwner,):
            return Course.objects.none()

        if self.request.user.groups.filter(name="Модератор").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)


class LessonsListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonsPaginator

    def get_queryset(self):

        if self.permission_classes != [IsModerator | IsOwner]:
            return Lesson.objects.none()
        if self.request.user.groups.filter(name="Модератор").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & IsModerator | IsAuthenticated & IsOwner]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & IsModerator | IsAuthenticated & IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & ~IsModerator | IsAuthenticated & IsOwner]
