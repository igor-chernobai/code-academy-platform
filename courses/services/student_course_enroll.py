from django.contrib.auth import get_user_model

from courses.models import Course

User = get_user_model()

def is_student_enrolled(course: Course, user: User) -> bool:
    return course.students.filter(id=user.id).exists()
