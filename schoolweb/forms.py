# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import StudentApplication

class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender', 'entry_grade',
            'parent_name', 'relationship', 'parent_email', 'parent_phone', 'home_address',
            'previous_school', 'current_grade', 'report_card',
            'confirm_accurate', 'confirm_policy'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'home_address': forms.Textarea(attrs={'rows': 3}),
            'confirm_accurate': forms.CheckboxInput(attrs={'required': True}),
            'confirm_policy': forms.CheckboxInput(attrs={'required': True}),
        }
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'date_of_birth': 'Date of birth',
            'entry_grade': 'Entry grade',
            'parent_name': 'Full name',
            'relationship': 'Relationship to student',
            'parent_email': 'Email address',
            'parent_phone': 'Phone number',
            'home_address': 'Home address',
            'previous_school': 'Current / most recent school',
            'current_grade': 'Current grade or class',
            'report_card': 'Upload most recent report card (PDF)',
            'confirm_accurate': 'I confirm the information given in this application is accurate to the best of my knowledge.',
            'confirm_policy': 'I have read the admissions policy and understand the ₦40,000 registration fee is non-refundable.',
        }
        error_messages = {
            'parent_email': {
                'invalid': 'Please enter a valid email address.',
                'required': 'Email address is required.',
            },
            'report_card': {
                'invalid_extension': 'Only PDF files are allowed.',
            }
        }
    
    def clean_report_card(self):
        report_card = self.cleaned_data.get('report_card')
        if report_card:
            # Check file size (10MB limit)
            if report_card.size > 10 * 1024 * 1024:
                raise ValidationError('File size must be under 10MB.')
        return report_card
    
    def clean(self):
        cleaned_data = super().clean()
        # Ensure both checkboxes are checked
        if not cleaned_data.get('confirm_accurate'):
            raise ValidationError('You must confirm that the information is accurate.')
        if not cleaned_data.get('confirm_policy'):
            raise ValidationError('You must read and accept the admissions policy.')
        return cleaned_data
    
   

