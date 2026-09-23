# models.py
from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
import uuid

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