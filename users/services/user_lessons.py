from django.contrib.auth import get_user_model

from courses.models import Course, Lesson
from users.models import StudentLastActivity

User = get_user_model()


def get_last_student_lesson(student: User, course: Course) -> Lesson:
    try:
        last_activity = StudentLastActivity.objects.get(student=student, course=course)
        return last_activity.last_lesson
    except StudentLastActivity.DoesNotExist:
        first_lesson = Lesson.objects.select_related("module__course").filter(module__course=course).first()
        return first_lesson
