from django.urls import path
from lms.apps import LmsConfig
from lms.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonsListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
)
from rest_framework.routers import DefaultRouter


app_name = LmsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", LessonsListAPIView.as_view(), name="lessons"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson"),
    path("lesson/new/", LessonCreateAPIView.as_view(), name="adding_lesson"),
    path("lesson/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="update_lesson"),
    path("lesson/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="delete_lesson"),
] + router.urls
