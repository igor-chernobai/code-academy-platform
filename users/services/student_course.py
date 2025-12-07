from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from courses.models import Course, Lesson
from users.models import StudentLastActivity

User = get_user_model()


def is_student_enrolled(course: Course, student: User) -> bool:
    return course.students.filter(id=student.id).exists()


# Отримання курсу
def get_course_for_student(student: User, course_id: int) -> Course:
    course_key = f"course_{course_id}_{student.id}"

    course = cache.get(course_key)
    if course is None:
        course = Course.objects.prefetch_related("modules__lessons").get(students=student, id=course_id)
        cache.set(course_key, course, 600)

    return course


def get_lesson_for_student(student: User, course: Course, lesson_slug: str) -> Lesson:
    lesson_key = f"lesson_{student.id}_{course.id}_{lesson_slug or 'last'}"

    lesson = cache.get(lesson_key)
    if lesson is None:
        if lesson_slug:
            lesson = get_object_or_404(Lesson.objects.select_related("module__course"),
                                       slug=lesson_slug,
                                       module__course=course)
        else:
            try:
                lesson = StudentLastActivity.objects.get(student=student, course=course).last_lesson
            except StudentLastActivity.DoesNotExist:
                lesson = Lesson.objects.select_related("module__course").filter(module__course=course).first()

    cache.set(lesson_key, lesson, 300)

    return lesson
