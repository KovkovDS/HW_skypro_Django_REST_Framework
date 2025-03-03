from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


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
