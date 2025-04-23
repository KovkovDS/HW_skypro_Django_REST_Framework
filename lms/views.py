from datetime import timedelta
from django.utils import timezone
from users.tasks import send_course_update_message
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from lms.models import Course, Lesson
from lms.paginators import LessonsPaginator, CoursesPaginator
from lms.serializer import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Класс представления вида ViewSet для эндпоинтов курса."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursesPaginator

    def get_permissions(self):
        """Метод получения разрешений на доступ к эндпоитам в соответствии с запросом."""

        if self.action in ["create"]:
            self.permission_classes = [IsAuthenticated & ~IsModerator]
        elif self.action in ["list", "change", "retrieve"]:
            self.permission_classes = [IsAuthenticated & IsOwner | IsAuthenticated & IsModerator]
        elif self.action in ["destroy"]:
            self.permission_classes = [IsAuthenticated & IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания "Курса"."""

        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

    def perform_update(self, serializer):
        """Метод вносит изменение в сериализатор редактирования "Курса"."""

        course = serializer.save()
        if course.updated_at:
            time_difference = timezone.now() - course.updated_at
            if time_difference > timedelta(hours=4):
                send_course_update_message.delay(course)
        else:
            send_course_update_message.delay(course)
        course.updated_at = timezone.now()
        course.save()

    def get_queryset(self):
        """Метод для изменения запроса к базе данных по объектам модели "Курса"."""

        if self.request.user.groups.filter(name="Модератор").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)


class LessonsListAPIView(generics.ListAPIView):
    """Класс представления вида Generic для эндпоинта списка уроков."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonsPaginator
    permission_classes = [IsAuthenticated & IsModerator | IsAuthenticated & IsOwner]

    def get_queryset(self):
        """Метод для изменения запроса к базе данных по объектам модели "Курса"."""

        if self.request.user.groups.filter(name="Модератор").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Класс представления вида Generic для эндпоинта списка уроков."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & IsModerator | IsAuthenticated & IsOwner]


class LessonCreateAPIView(generics.CreateAPIView):
    """Класс представления вида Generic для эндпоинта создания урока."""

    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания "Урока"."""

        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Класс представления вида Generic для эндпоинта изменения урока."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & IsModerator | IsAuthenticated & IsOwner]

    def perform_update(self, serializer):
        """Метод вносит изменение в сериализатор редактирования "Урока"."""

        lesson = serializer.save()
        courses = Course.objects.filter(pk=lesson.course.pk)
        # course_serializer = CourseSerializer()
        for course in courses:
            if lesson.updated_at:
                time_difference = timezone.now() - lesson.updated_at
                if time_difference > timedelta(hours=4):
                    send_course_update_message.delay(course.pk)
                    # send_course_update_for_update_lesson_message.delay(lesson.pk)
                    # lesson.updated_at = timezone.now()
                    # course.updated_at = timezone.now()
            else:
                send_course_update_message.delay(course.pk)
        # send_course_update_for_update_lesson_message.delay(lesson.pk)
        lesson.updated_at = timezone.now()
        courses.updated_at = timezone.now()
        lesson.save()
        # course_serializer.is_valid(data=course)
        # course_serializer.save()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Класс представления вида Generic для эндпоинта удаления урока."""

    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & ~IsModerator | IsAuthenticated & IsOwner]
