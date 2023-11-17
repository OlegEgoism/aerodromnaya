from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from rangefilter.filters import DateRangeFilterBuilder

from partnership.models import InfoChairman, FeedbackJob, Photo

"""Убираем отображение в админке"""
admin.site.unregister(Group)


class PhotoInline(admin.TabularInline):
    """Фотография"""
    model = Photo
    extra = 0
    readonly_fields = 'preview', 'photo',
    classes = ['collapse']

    def preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="600" height="600" />')
        else:
            return 'Нет фотографии'

    preview.short_description = 'Фотография'

    def has_add_permission(self, request, obj=None):
        return False  # Запрещаем создание новых объектов

    def has_delete_permission(self, request, obj=None):
        return False  # Запрещаем удаление существующих объектов


@admin.register(InfoChairman)
class InfoChairmanAdmin(admin.ModelAdmin):
    """Контакты председателя"""
    list_display = '__str__', 'phone', 'time_start', 'time_end',
    list_editable = 'time_start', 'time_end',

    def has_add_permission(self, request):  # позволяет создать только одну модель
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(FeedbackJob)
class FeedbackJobAdmin(admin.ModelAdmin):
    """Заявки"""
    list_display = '__str__', 'short_message', 'datetime_start', 'status', 'datetime_end',
    fields = 'status', 'datetime_end', 'message_comment', 'last_name', 'first_name', 'middle_name', 'apartment', 'entrance', 'phone', 'message', 'datetime_start',
    readonly_fields = 'last_name', 'first_name', 'middle_name', 'apartment', 'entrance', 'phone', 'message', 'datetime_start', 'datetime_end',
    list_editable = 'status',
    list_filter = 'status', ('datetime_start', DateRangeFilterBuilder()), ('datetime_end', DateRangeFilterBuilder()),
    search_fields = 'last_name', 'first_name', 'middle_name', 'phone',
    search_help_text = 'Поиск по ФИО и телефону'
    date_hierarchy = 'datetime_start'
    inlines = PhotoInline,
    list_per_page = 10

    def short_message(self, obj):
        return (obj.message[:200] + '...') if len(obj.message) > 200 else obj.message

    short_message.short_description = 'Краткое сообщение'

# @admin.register(Photo)
# class PhotoAdmin(admin.ModelAdmin):
#     """Фотография"""
#     list_display = 'feedback_job', 'photo', 'preview'
#
#     def preview(self, obj):
#         if obj.photo:
#             return mark_safe(f'<img src="{obj.photo.url}" width="60" height="60" />')
#         else:
#             return 'Нет фотографии'
#
#     preview.short_description = 'Фотография'
