from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from lms.models import Course, Lesson
from users.models import User, SubscriptionForCourse


class TestCase(APITestCase):
    """Базовый тестовый класс для всех тестов."""

    def setUp(self):
        """Задает начальные данные для тестов."""

        self.user = User.objects.create(email="admin@sky.pro")
        link_to_video = 'https://www.youtube.com/'
        self.course = Course.objects.create(title="Test Course for tests", description='Test Course for tests',
                                            owner=self.user)
        self.lesson = Lesson.objects.create(title="Test Lesson for tests", description='Test Lesson for tests',
                                            course=self.course, link_to_video=link_to_video, owner=self.user)
        self.client.force_authenticate(user=self.user)


class SubscriptionForCourseViewTestCase(TestCase, APITestCase):
    """Тесты на добавление подписки на курс."""

    def test_subscription_create(self):
        """Тест на добавление подписки на курс."""

        url = reverse("users:subscription")
        data = {"owner": self.user.pk, "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Подписка добавлена.'})

    def test_subscription_delete(self):
        """Тест на удаление подписки на курс."""

        self.subscription = SubscriptionForCourse.objects.create(course=self.course, owner=self.user)
        data = {"owner": self.user.id,"course": self.course.id}
        url = reverse("users:subscription")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Подписка удалена.'})
