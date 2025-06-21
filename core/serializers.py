from rest_framework import serializers
from .models import Category, Course, Lesson, Material, Enrollment, QuestionAnswer, LessonProgress

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )

    class Meta:
        model = Enrollment
        fields = '__all__'

class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
  

    class Meta:
        model = Lesson
        fields = '__all__'  # or list all fields + 'completed'

    def get_completed(self, obj):
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return False
        user = request.user
        from .models import Enrollment, LessonProgress
        try:
            enrollment = Enrollment.objects.get(user=user, course=obj.course)
            progress = LessonProgress.objects.filter(
                enrollment=enrollment, lesson=obj, is_completed=True
            ).exists()
            return progress
        except Enrollment.DoesNotExist:
            return False