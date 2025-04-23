from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.fields import DateTimeField, DecimalField
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from lms.models import Course, Lesson
from users.models import User, SubscriptionForCourse, Payments


class TestCase(APITestCase):
    """Базовый тестовый класс для всех тестов."""

    def setUp(self):
        """Задает начальные данные для тестов."""

        self.user = User.objects.create(email="admin@sky.pro")
        self.administrator_group = Group.objects.create(name="Администратор")
        self.user.groups.add(self.administrator_group)
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
        self.payment = Payments.objects.create(
            owner=self.user,
            paid_course=self.course,
            paid_lesson=self.lesson,
            payment_amount=25000.00,
            payment_method="CASH",
        )
        self.client.force_authenticate(user=self.user)


class SubscriptionForCourseViewTestCase(TestCase, APITestCase):
    """Тесты на добавление подписки на курс."""

    def test_subscription_create(self):
        """Тест на добавление подписки на курс."""

        url = reverse("users:subscription")
        data = {"owner": self.user.pk, "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Подписка добавлена."})

    def test_subscription_delete(self):
        """Тест на удаление подписки на курс."""

        self.subscription = SubscriptionForCourse.objects.create(course=self.course, owner=self.user)
        data = {"owner": self.user.id, "course": self.course.id}
        url = reverse("users:subscription")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Подписка удалена."})


class ProfileTestCase(TestCase, APITestCase):
    """Тесты для работы с пользователями."""

    def test_list_profiles(self):
        """Тест на получение списка пользователей."""

        url = reverse("users:profiles")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = [
            {
                "id": self.user.pk,
                "email": self.user.email,
                "avatar": self.user.avatar,
                "phone_number": self.user.phone_number,
                "city": self.user.city,
            }
        ]
        self.assertEqual(data, result)

    def test_retrieve_profile(self):
        """Тест получения пользователя по Primary Key."""

        url = reverse("users:profile", args=(self.user.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["email"], self.user.email)

    def test_create_profile(self):
        """Тест создания нового пользователя."""

        url = reverse("users:registration")
        data = {"email": "test_user__for_test@sky.pro", "password": "test_user12345"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(email="test_user__for_test@sky.pro").count(), 1)
        self.assertTrue(User.objects.all().exists())

    def test_update_profile(self):
        """Тест изменения пользователя по Primary Key."""

        url = reverse("users:update_profile", args=(self.user.pk,))
        data = {
            "email": "updated_test_user__for_test@sky.pro",
            "password": "test_user123456",
            "phone_number": "79865432112",
            "city": "Volgograd",
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.user.pk).city, "Volgograd")

    def test_delete_profile(self):
        """Тест удаления пользователя по Primary Key."""

        url = reverse("users:delete_profile", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)


class PaymentsTestCase(TestCase, APITestCase):
    """Тесты для работы с платежами."""

    def test_list_payments(self):
        """Тест на получение списка платежей."""

        res_created_at = DateTimeField().to_representation
        res_payment_amount = DecimalField(
            decimal_places=2,
            max_digits=9,
        ).to_representation
        url = reverse("users:payments")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = [
            {
                "id": self.payment.pk,
                "created_at": res_created_at(self.payment.created_at),
                "payment_amount": res_payment_amount(self.payment.payment_amount),
                "payment_method": self.payment.payment_method,
                "session_id": None,
                "payment_link": None,
                "owner": self.user.pk,
                "paid_course": self.course.pk,
                "paid_lesson": self.lesson.pk,
            }
        ]
        self.assertEqual(data, result)

    def test_retrieve_payment(self):
        """Тест получения платежа по Primary Key."""

        url = reverse("users:payment", args=(self.payment.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["owner"], self.payment.owner.pk)

    def test_create_payments(self):
        """Тест создания новой оплаты."""

        url = reverse("users:adding_payment")
        data = {
            "owner": self.user.pk,
            "payment_amount": 35000.00,
            "payment_method": "TRANSFER",
            "paid_course": self.course.pk,
            "paid_lesson": self.lesson.pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payments.objects.filter(payment_amount=35000.00).count(), 1)
        self.assertTrue(Payments.objects.all().exists())

    def test_update_payment(self):
        """Тест изменения платежа по Primary Key."""

        url = reverse("users:update_payment", args=(self.payment.pk,))
        data = {
            "owner": self.user.pk,
            "payment_amount": 30000.00,
            "payment_method": "CASH",
            "paid_course": self.course.pk,
            "paid_lesson": self.lesson.pk,
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Payments.objects.get(pk=self.payment.pk).payment_amount, 30000.00)

    def test_delete_payment(self):
        """Тест удаления оплаты по Primary Key."""

        url = reverse("users:delete_payment", args=(self.payment.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Payments.objects.count(), 0)
