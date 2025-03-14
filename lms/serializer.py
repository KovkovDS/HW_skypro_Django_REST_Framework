from rest_framework import serializers
from lms.models import Course, Lesson
from lms.validators import LinkOnVideoValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        # depth = 1
        validators = [LinkOnVideoValidator(field='link_to_video')]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lesson_information = LessonSerializer(source='lesson_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        # depth = 1

    def get_count_lessons(self, instance):
        return Lesson.objects.filter(course=instance).count()

