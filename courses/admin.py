from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline

from courses.models import Course, Lesson, Module


class ModuleInline(StackedInline):
    model = Module
    tab = True


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ["title", "owner", "created"]
    prepopulated_fields = {"slug": ["title"]}
    compressed_fields = True
    filter_horizontal = ["students"]

    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(ModelAdmin):
    list_display = ["course", "title", "created", "order"]
    list_display_links = ["title"]
    ordering = ["order"]
    prepopulated_fields = {'slug': ["title"]}
    compressed_fields = True


@admin.register(Lesson)
class LessonAdmin(ModelAdmin):
    list_display = ["module", "title", "created", "order"]
    list_display_links = ["title"]
    ordering = ["order"]
    compressed_fields = True
    prepopulated_fields = {'slug': ["title"]}
    search_fields = ["title"]
    list_filter = ["module"]
    warn_unsaved_form = True
