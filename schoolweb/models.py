# models.py
from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
import uuid
from django.utils import timezone
from django.conf import settings


class StudentApplication(models.Model):
    # Generate unique reference number
    reference_number = models.CharField(max_length=20, unique=True, editable=False)
    
    # Student details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    GRADE_CHOICES = [
        ('6', 'Grade 6'),
        ('7', 'Grade 7'),
        ('8', 'Grade 8'),
        ('9', 'Grade 9'),
        ('10', 'Grade 10'),
        ('11', 'Grade 11'),
    ]
    entry_grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    
    # Parent/Guardian details
    parent_name = models.CharField(max_length=200)
    RELATION_CHOICES = [
        ('Mother', 'Mother'),
        ('Father', 'Father'),
        ('Guardian', 'Guardian'),
    ]
    relationship = models.CharField(max_length=50, choices=RELATION_CHOICES)
    parent_email = models.EmailField()
    parent_phone = models.CharField(max_length=20)
    home_address = models.TextField()
    
    # Previous school
    previous_school = models.CharField(max_length=200)
    current_grade = models.CharField(max_length=50, blank=True)
    report_card = models.FileField(
        upload_to='report_cards/',
        validators=[FileExtensionValidator(['pdf'])],
        blank=True,
        null=True
    )
    
    # Terms and conditions
    confirm_accurate = models.BooleanField(default=False)
    confirm_policy = models.BooleanField(default=False)
    
    # Status and timestamps
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.reference_number:
            # Generate unique reference number: SV-YYYY-XXXX
            year = self.submitted_at.year if self.submitted_at else 2026
            unique_id = str(uuid.uuid4())[:8].upper()
            self.reference_number = f"NH-{year}-{unique_id}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.reference_number}"
    
    class Meta:
        ordering = ['-submitted_at']

class StudentProfile(models.Model):
    CLASS_CHOICES = [
        ('JSS1', 'JSS 1'), ('JSS2', 'JSS 2'), ('JSS3', 'JSS 3'),
        ('SSS1', 'SSS 1'), ('SSS2', 'SSS 2'), ('SSS3', 'SSS 3'),
    ]
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
    )
    admission_number = models.CharField(max_length=20, unique=True)
    student_class = models.CharField(max_length=10, choices=CLASS_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    guardian_name = models.CharField(max_length=150, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)
    enrolled_on = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['student_class', 'admission_number']

    def __str__(self):
        name = self.user.get_full_name() or self.user.username
        return f"{name} ({self.admission_number})"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Result(models.Model):
    TERM_CHOICES = [
        ('1st', 'First Term'),
        ('2nd', 'Second Term'),
        ('3rd', 'Third Term'),
    ]

    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name='results'
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.PROTECT, related_name='results'
    )
    term = models.CharField(max_length=5, choices=TERM_CHOICES)
    session = models.CharField(max_length=9, help_text="e.g. 2025/2026")
    ca_score = models.PositiveSmallIntegerField(default=0)
    exam_score = models.PositiveSmallIntegerField(default=0)
    remark = models.CharField(max_length=150, blank=True)
    recorded_on = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('student', 'subject', 'term', 'session')
        ordering = ['-session', 'term', 'subject__name']

    @property
    def total(self):
        return self.ca_score + self.exam_score

    @property
    def grade(self):
        t = self.total
        if t >= 75: return 'A'
        if t >= 65: return 'B'
        if t >= 55: return 'C'
        if t >= 45: return 'D'
        if t >= 40: return 'E'
        return 'F'

    def __str__(self):
        return f"{self.student} — {self.subject} — {self.term} {self.session} ({self.total})"
        


