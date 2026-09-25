# admin.py
from django.contrib import admin
from .models import StudentApplication, StudentProfile, Subject, Result


@admin.register(StudentApplication)
class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'first_name', 'last_name', 'entry_grade', 'status', 'submitted_at']
    list_filter = ['status', 'entry_grade', 'gender']
    search_fields = ['reference_number', 'first_name', 'last_name', 'parent_email']
    readonly_fields = ['reference_number', 'submitted_at', 'updated_at']
    fieldsets = (
        ('Application Info', {
            'fields': ('reference_number', 'status', 'submitted_at', 'updated_at')
        }),
        ('Student Details', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 'entry_grade')
        }),
        ('Parent/Guardian Details', {
            'fields': ('parent_name', 'relationship', 'parent_email', 'parent_phone', 'home_address')
        }),
        ('Previous School', {
            'fields': ('previous_school', 'current_grade', 'report_card')
        }),
        ('Terms', {
            'fields': ('confirm_accurate', 'confirm_policy')
        }),
    )
    
    

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'full_name', 'student_class', 'gender', 'enrolled_on')
    list_filter = ('student_class', 'gender')
    search_fields = ('admission_number', 'user__username', 'user__first_name', 'user__last_name')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'term', 'session', 'ca_score', 'exam_score', 'total', 'grade')
    list_filter = ('session', 'term', 'subject')
    search_fields = ('student__admission_number', 'student__user__first_name', 'student__user__last_name')
    autocomplete_fields = ('student', 'subject')