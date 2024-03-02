from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Tawassut, Kafeel, Course, Class, Section, Student, Progress

@admin.register(Tawassut)
class TawassutAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address')

@admin.register(Kafeel)
class KafeelAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'phone', 'address', 'tawassut_link')

    def tawassut_link(self, obj):
        return format_html('<a href="{}">{}</a>', reverse('admin:kifalat_tawassut_change', args=[obj.tawassut.id]), obj.tawassut)
    tawassut_link.short_description = 'Tawassut'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'name', 'father_name', 'phone', 'course', 'class_field', 'section', 'kafeel_link', 'sponsoring_since', 'status')
    list_filter = ('course', 'class_field', 'section', 'kafeel', 'kafeel__tawassut', 'status')
    search_fields = ('name', 'father_name', 'phone')

    def kafeel_link(self, obj):
        if obj.kafeel:
            return format_html('<a href="{}">{}</a>', reverse('admin:kifalat_kafeel_change', args=[obj.kafeel.id]), obj.kafeel)
        else:
            return None

    kafeel_link.short_description = 'Kafeel'

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('kafeel', 'student', 'receipt_number', 'amount_paid', 'study_report', 'paid_date')
    list_filter = ('kafeel', 'student', 'student__course', 'student__class_field', 'student__section', 'paid_date')
    search_fields = ('receipt_number', 'study_report')
