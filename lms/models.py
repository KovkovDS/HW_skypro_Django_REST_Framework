from django.core.validators import FileExtensionValidator
from django.db import models
from HW_skypro_Django_REST_Framework import settings


class Course(models.Model):
    """Класс модели "Курс"."""

    title = models.CharField(max_length=100, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="lms/courses/pictures",
        null=True,
        blank=True,
        verbose_name="Превью курса",
        validators=[
            FileExtensionValidator(
                ["jpg", "png"],
                "Расширение файла « %(extension)s » не допускается. "
                "Разрешенные расширения: %(allowed_extensions)s .",
                "Недопустимое расширение!",
            )
        ],
    )
    description = models.TextField(null=True, blank=True, verbose_name="Описание курса")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Владелец"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        """Метод для описания человеко читаемого вида модели "Курс"."""

        return f"Название курса: {self.title}. Описание курса: {self.description}."

    class Meta:
        """Класс для изменения поведения полей модели "Курс"."""

        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["id", "updated_at", "owner", "title"]


class Lesson(models.Model):
    """Класс модели "Урок"."""

    title = models.CharField(max_length=100, verbose_name="Название урока")
    description = models.TextField(null=True, blank=True, verbose_name="Описание урока")
    preview = models.ImageField(
        upload_to="lms/lessons/pictures",
        null=True,
        blank=True,
        verbose_name="Превью урока",
        validators=[
            FileExtensionValidator(
                ["jpg", "png"],
                "Расширение файла « %(extension)s » не допускается. "
                "Разрешенные расширения: %(allowed_extensions)s .",
                "Недопустимое расширение!",
            )
        ],
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lessons")
    link_to_video = models.CharField(max_length=150, verbose_name="Ссылка на видео урока")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Владелец"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        """Метод для описания человеко читаемого вида модели "Урок"."""

        return (
            f"Название урока: {self.title}. Описание урока: {self.description}. Курс: "
            f"{self.course.title}. Ссылка на видео урока: {self.link_to_video}."
        )

    class Meta:
        """Класс для изменения поведения полей модели "Урок"."""

        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["id", "updated_at", "owner", "course", "title"]
