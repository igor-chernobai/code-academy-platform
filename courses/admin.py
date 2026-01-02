from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline

from courses import models


class ModuleInline(StackedInline):
    model = models.Module
    tab = True


@admin.register(models.Course)
class CourseAdmin(ModelAdmin):
    list_display = ['title', 'owner', 'get_count_students', 'created']
    list_display_links = ['title', 'owner']
    prepopulated_fields = {'slug': ['title']}
    filter_horizontal = ['students']

    inlines = [ModuleInline]

    compressed_fields = True

    @admin.display(description='Кількість записаних студентів')
    def get_count_students(self, obj):
        return obj.students.count()


@admin.register(models.Module)
class ModuleAdmin(ModelAdmin):
    list_display = ['course', 'title', 'created', 'order', 'get_count_lessons']
    list_display_links = ['title']
    ordering = ['order']
    prepopulated_fields = {'slug': ['title']}

    compressed_fields = True

    @admin.display(description='Кількість лекцій')
    def get_count_lessons(self, obj):
        return obj.lessons.count()


@admin.register(models.Lesson)
class LessonAdmin(ModelAdmin):
    list_display = ['module', 'title', 'order', 'get_count_content', 'created']
    list_display_links = ['title']
    list_filter = ['module']
    ordering = ['order']
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['title', 'module__title']
    fields = ['module', 'title', 'slug', 'order', 'content']
    readonly_fields = ['created']

    compressed_fields = True
    warn_unsaved_form = True

    @admin.display(description='Кількість елементів')
    def get_count_content(self, obj):
        return len(obj.content)


@admin.register(models.Review)
class ReviewAdmin(ModelAdmin):
    list_display = ['student', 'course', 'rating']
    list_display_links = ['student', 'course']
    list_filter = ['rating', 'course']
    readonly_fields = ['created_at']
    search_fields = ['student__email']

    compressed_fields = True
