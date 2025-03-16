from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from lms.models import Course, Lesson


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Адрес электронной почты должен быть указан")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Адрес электронной почты')
    avatar = models.ImageField(upload_to='users/images', null=True, blank=True, verbose_name='Аватар профиля',
                               validators=[FileExtensionValidator(['jpg', 'png'],
                                                                  'Расширение файла « %(extension)s » не допускается. ' 
                                                                  'Разрешенные расширения: %(allowed_extensions)s .' 
                                                                  'Недопустимое расширение!')])
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name='Номер телефона')
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')
    username = None
    token = models.CharField(max_length=150, blank=True, null=True, verbose_name='Токен для верификации')
    create_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email', 'phone_number', 'updated_at']


class Payments(models.Model):
    PAYMENT_METHOD_CHOICES = [('CASH', 'Наличные',), ('TRANSFER', 'Перевод на счет',)]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name='Оплаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name='Оплаченный урок')
    payment_amount = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.owner} = {self.payment_amount} ({self.payment_method})'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['created_at', 'owner', 'payment_amount', 'paid_course', 'paid_lesson', 'payment_method']


class SubscriptionForCourse(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Подписка на курс')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата начала подписки')

    def __str__(self):
        return f'{self.owner}: {self.course} {self.course.title}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['created_at', 'owner', 'course']
