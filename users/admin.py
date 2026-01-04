from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm

from subscriptions.admin import SubscriptionHistoryTabular, SubscriptionTabular
from users.forms import CustomUserCreationForm
from users.models import StudentLastActivity, StudentProgress

admin.site.unregister(Group)


@admin.register(get_user_model())
class UserAdmin(UserAdmin, ModelAdmin):
    readonly_fields = ['last_login', 'date_joined']
    compressed_fields = True
    fieldsets = (

        (_('Personal info'), {
            'classes': ['tab'],
            'fields': ('email', 'password', 'first_name', 'last_name', 'last_login', 'date_joined')}),
        (
            _('Permissions'),
            {
                'classes': ['tab'],
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'first_name', 'last_name', 'password', 'password2'),
            },
        ),
    )
    list_display = ('email', 'get_full_info', 'is_staff', 'get_user_subscription')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    list_select_related = ['subscription__plan']
    filter_horizontal = (
        'groups',
        'user_permissions',
    )
    ordering = ('email',)
    form = UserChangeForm
    add_form = CustomUserCreationForm
    change_password_form = AdminPasswordChangeForm

    inlines = [SubscriptionTabular, SubscriptionHistoryTabular]

    @admin.display(description='Ім`я та фамілія')
    def get_full_info(self, obj):
        return obj.get_full_name()

    @admin.display(description='Підписка')
    def get_user_subscription(self, obj):
        status = 'Активна' if obj.subscription.is_active else 'Не активна'
        return f'{obj.subscription.plan.name} | {status}'


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(StudentLastActivity)
class StudentStudentLastActivity(ModelAdmin):
    list_display = ['student', 'course', 'last_lesson', 'last_viewed']
    readonly_fields = ['last_viewed']
    list_display_links = ['course', 'last_lesson']
    compressed_fields = True
    list_filter = ['student', 'course']


@admin.register(StudentProgress)
class StudentLessonProgressAdmin(ModelAdmin):
    list_display = ['student', 'lesson', 'is_complete']
    readonly_fields = ['complete_at']
