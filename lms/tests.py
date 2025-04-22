from rest_framework.fields import DateTimeField
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from lms.models import Course, Lesson
from users.models import User


class TestCase(APITestCase):
    """Базовый тестовый класс для всех тестов."""

    def setUp(self):
        """Задает начальные данные для тестов."""

        self.user = User.objects.create(email="admin@sky.pro")
        link_to_video = "https://www.youtube.com/"
        self.course = Course.objects.create(
            title="Test Course for tests", description="Test Course for tests", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson for tests",
            description="Test Lesson for tests",
            course=self.course,
            link_to_video=link_to_video,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)


class CourseTestCase(TestCase, APITestCase):
    """Тесты для работы с курсами."""

    def test_course_list(self):
        """Тест на получение списка курсов."""

        res_created_at = DateTimeField().to_representation
        res_updated_at = DateTimeField().to_representation
        url = reverse("lms:courses-list")
        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "count_lessons": 1,
                    "lesson_information": [
                        {
                            "id": self.lesson.pk,
                            "title": self.lesson.title,
                            "description": self.lesson.description,
                            "preview": None,
                            "link_to_video": self.lesson.link_to_video,
                            "created_at": res_created_at(self.lesson.created_at),
                            "updated_at": res_updated_at(self.lesson.updated_at),
                            "course": self.course.pk,
                            "owner": self.user.pk,
                        }
                    ],
                    "subscription": False,
                    "count_subscriptions": "Подписок - 0.",
                    "title": self.course.title,
                    "preview": None,
                    "description": self.course.description,
                    "owner": self.user.pk,
                    "created_at": res_created_at(self.course.created_at),
                    "updated_at": res_updated_at(self.course.updated_at),
                }
            ],
        }
        #
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_retrieve_course(self):
        """Тест получения курса по Primary Key."""

        url = reverse("lms:courses-detail", args=[self.course.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(Course.objects.all().count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_create_course(self):
        """Тест создания нового курса."""

        url = reverse("lms:courses-list")
        data = {"title": "Test Course for tests 2", "description": "Test Course for tests 2", "owner": self.user.pk}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.filter(title="Test Course for tests 2").count(), 1)
        self.assertTrue(Course.objects.all().exists())

    def test_update_course(self):
        """Тест изменения курса по Primary Key."""

        url = reverse("lms:courses-detail", args=(self.course.pk,))
        data = {
            "title": "Updated Test Course for tests",
            "description": "Updated Test Course for tests",
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.get(pk=self.course.pk).title, "Updated Test Course for tests")

    def test_delete_course(self):
        """Тест удаления курса по Primary Key."""

        url = reverse("lms:courses-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class LessonTestCase(TestCase, APITestCase):
    """Тесты для работы с уроками."""

    def test_lesson_list(self):
        """Тест на получение списка уроков."""

        res_created_at = DateTimeField().to_representation
        res_updated_at = DateTimeField().to_representation
        url = reverse("lms:lessons")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "link_to_video": self.lesson.link_to_video,
                    "created_at": res_created_at(self.lesson.created_at),
                    "updated_at": res_updated_at(self.lesson.updated_at),
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(data, result)

    def test_retrieve_lesson(self):
        """Тест получения урока по Primary Key."""

        url = reverse("lms:lesson", args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], self.lesson.title)

    def test_create_lesson(self):
        """Тест создания нового урока."""

        url = reverse("lms:adding_lesson")
        data = {
            "title": "Test Lesson for tests 2",
            "description": "Test Lesson for tests 2",
            "link_to_video": "https://www.youtube.com/lesson_1",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.filter(description="Test Lesson for tests 2").count(), 1)
        self.assertTrue(Lesson.objects.all().exists())

    def test_update_lesson(self):
        """Тест изменения урока по Primary Key."""

        url = reverse("lms:update_lesson", args=(self.lesson.pk,))
        data = {
            "title": "Updated Test Lesson for tests",
            "description": "Updated Test Lesson for tests 2",
            "link_to_video": "https://www.youtube.com/lesson_1",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(pk=self.lesson.pk).description, "Updated Test Lesson for tests 2")

    def test_lesson_delete(self):
        """Тест удаления урока по Primary Key."""

        url = reverse("lms:delete_lesson", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)
