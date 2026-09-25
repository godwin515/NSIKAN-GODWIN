# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import StudentApplication, StudentProfile, Result
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

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
    


class StudentLoginForm(forms.Form):
    identifier = forms.CharField(
        label='Admission Number / Username / Email',
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. NH/2026/001',
            'autocomplete': 'username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
            'autocomplete': 'current-password',
        })
    )
    remember_me = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned = super().clean()
        identifier = (cleaned.get('identifier') or '').strip()
        password = cleaned.get('password')

        if identifier and password:
            username = identifier

            # 1) Try admission number
            profile = StudentProfile.objects.filter(
                admission_number__iexact=identifier
            ).select_related('user').first()
            if profile:
                username = profile.user.username
            # 2) Try email
            elif '@' in identifier:
                try:
                    u = User.objects.get(email__iexact=identifier)
                    username = u.username
                except User.DoesNotExist:
                    pass

            self.user = authenticate(self.request, username=username, password=password)

            if self.user is None:
                raise forms.ValidationError(
                    "Invalid credentials. Check your admission number and password."
                )
            if not self.user.is_active:
                raise forms.ValidationError(
                    "This account is disabled. Contact the school office."
                )
            if not hasattr(self.user, 'student_profile'):
                raise forms.ValidationError(
                    "This account is not a student account."
                )
        return cleaned


class ResultLookupForm(forms.Form):
    session = forms.ChoiceField(required=False)
    term = forms.ChoiceField(
        required=False,
        choices=[('', 'All terms')] + Result.TERM_CHOICES,
    )

    def __init__(self, *args, session_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [('', 'All sessions')]
        if session_choices:
            choices += [(s, s) for s in session_choices]
        self.fields['session'].choices = choices