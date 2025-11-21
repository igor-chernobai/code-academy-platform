from django.contrib import admin

from unfold.admin import ModelAdmin

from courses.models import Course, Module, Lesson, LessonProgress


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ["title", "owner", "created"]
    compressed_fields = True


@admin.register(Module)
class ModuleAdmin(ModelAdmin):
    list_display = ["course", "title", "created", "order"]
    compressed_fields = True
    prepopulated_fields = {'slug': ["title"]}


@admin.register(Lesson)
class LessonAdmin(ModelAdmin):
    list_display = ["module", "title", "created", "order"]
    compressed_fields = True
    prepopulated_fields = {'slug': ["title"]}


@admin.register(LessonProgress)
class LessonProgressAdmin(ModelAdmin):
    list_display = ["student", "lesson", "is_complete"]
    readonly_fields = ["complete_at"]
