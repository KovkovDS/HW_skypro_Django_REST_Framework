from rest_framework import serializers
from lms.models import Course, Lesson
from lms.validators import LinkOnVideoValidator
from users.models import SubscriptionForCourse, User


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkOnVideoValidator(field='link_to_video')]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField(read_only=True)
    lesson_information = LessonSerializer(source='lessons', many=True, read_only=True)
    subscription = serializers.SerializerMethodField(read_only=True)
    count_subscriptions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lessons(self, instance):
        return Lesson.objects.filter(course=instance).count()

    def get_count_subscriptions(self, instance):
        return f'Подписок - {SubscriptionForCourse.objects.filter(course=instance).count()}.'

    def get_subscription(self, instance):
        user = self.context['request'].user
        subscription = SubscriptionForCourse.objects.all().filter(owner=user, course=instance).exists()
        if subscription:
            return f'У Вас есть подписка на данный курс.'
        return False

