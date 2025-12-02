from django.contrib.auth import get_user_model
from django.db import models

from courses.models import Course, Lesson


class StudentLastActivity(models.Model):
    student = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="студент"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="курс"
    )
    last_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="last_lesson",
        verbose_name="остання лекція"
    )
    last_viewed = models.DateTimeField("дата останнього просмотру", auto_now=True)

    class Meta:
        db_table = "student_last_activities"
        verbose_name = "остання активність"
        verbose_name_plural = "останні активності"

        constraints = [
            models.UniqueConstraint(fields=["student", "course"], name="unique_student_activity")
        ]

    def __str__(self):
        return f"Остання активність: {self.student.get_full_name()}"


class StudentProgress(models.Model):
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="користувач")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="лекція")
    is_complete = models.BooleanField("завершено?")
    complete_at = models.DateTimeField("дата завершення лекції", auto_now_add=True)

    class Meta:
        db_table = "lesson_progress"
        verbose_name = "прогрес лекції"
        verbose_name_plural = "прогрес лекцій"

        constraints = [
            models.UniqueConstraint(fields=["student", "lesson"], name="unique_student_progress")
        ]

    def __str__(self):
        status = "Завершено" if self.is_complete else "Не завершено"
        return f"{self.student} - {self.lesson} ({status})"
