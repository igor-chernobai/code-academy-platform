from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from courses.models import Course, Lesson
from users.models import StudentProgress

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


def get_lesson_by_slug(course_id: int, lesson_slug: str):
    lesson = get_object_or_404(
        Lesson.objects.select_related("module__course"), slug=lesson_slug, module__course_id=course_id
    )
    return lesson


def get_first_uncompleted_lesson(student: User, course_id: int):
    lessons_id = (
        StudentProgress.objects.select_related("lesson__module__course_id")
        .filter(student=student, is_complete=True, lesson__module__course_id=course_id)
        .values_list("lesson_id", flat=True)
    )

    lessons = (
        Lesson.objects.filter(module__course_id=course_id).exclude(id__in=lessons_id).order_by("module__order", "order")
    )

    return lessons.first()


def complete_lesson(student: User, lesson_id: int):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    obj, created = StudentProgress.objects.get_or_create(lesson=lesson, student=student, defaults={"is_complete": True})

    return obj
