# admin.py
from django.contrib import admin
from .models import StudentApplication

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