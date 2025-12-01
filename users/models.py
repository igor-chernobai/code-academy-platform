from django.contrib.auth import get_user_model
from django.db import models

from courses.models import Lesson, Course


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
