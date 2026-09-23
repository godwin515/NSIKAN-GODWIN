from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .forms import StudentApplicationForm
from .models import StudentApplication
from django.http import HttpResponse


# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')    

def admissions(request):
    return render(request, 'admissions.html')

def academics(request):
    return render(request, 'academics.html')

def contact(request):
    return render(request, 'contact.html')

def events(request):
    return render(request, 'events.html')


# # def apply(request):
#     if request.method == 'POST':
#         form = StudentApplicationForm(request.POST, request.FILES)
#         if form.is_valid():
#             application = form.save()
            
#             # Send confirmation email
#             try:
#                 send_mail(
#                     f'Application Confirmation - {application.reference_number}',
#                     f"""
#                     Dear {application.parent_name},

#                     Thank you for submitting an application for {application.first_name} {application.last_name}.

#                     Reference Number: {application.reference_number}

#                     Next Steps:
#                     1. You will receive an entrance-assessment date within five working days
#                     2. Our admissions office will contact you

#                     Best regards,
#                     Suryodaya Valley Secondary School
#                     """,
#                     settings.DEFAULT_FROM_EMAIL,
#                     [application.parent_email],
#                     fail_silently=False,
#                 )
#             except Exception as e:
#                 # Log the error but don't stop the submission
#                 print(f"Email sending error: {e}")
            
#             messages.success(request, f'Application submitted! Reference: {application.reference_number}')
#             return redirect('application_success', reference=application.reference_number)
    
#     form = StudentApplicationForm()
#     return render(request, 'apply.html', {'form': form})

def apply(request):
    if request.method == 'POST':
        form = StudentApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            
            # Send confirmation email
            send_confirmation_email(application)
            
            messages.success(
                request, 
                f'Your application has been submitted successfully! Your reference number is {application.reference_number}.'
            )
            return redirect('application_success', reference=application.reference_number)
        # else:
        #     messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentApplicationForm()
    
    return render(request, 'apply.html', {'form': form})

def application_success(request, reference):
    application = get_object_or_404(StudentApplication, reference_number=reference)
    return render(request, 'application_success.html', {'application': application})

def send_confirmation_email(application):
    subject = f'Application Confirmation - {application.reference_number}'
    message = f"""
    Dear {application.parent_name},

    Thank you for submitting an application for {application.first_name} {application.last_name} to New Heaven Secondary School.

    Reference Number: {application.reference_number}

    Next Steps:
    1. You will receive an entrance-assessment date within five working days.
    2. Our admissions office will contact you regarding the next steps.
    3. Please ensure you have your reference number ready for all future communications.

    For any questions, please contact:
    admissions@newheaveny.edu
    +234 000 000 0000

    Best regards,
     New Heaven School
    Admissions Office
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [application.parent_email],
            fail_silently=False,
        )
    except Exception as e:
        # Log the error but don't stop the process
        print(f"Email sending failed: {e}")


def test_email(request):
    try:
        send_mail(
            'Test Email from New Heaven',
            'This is a test email to verify the Django email configuration is working correctly.',
            settings.DEFAULT_FROM_EMAIL,
            ['godwinnsikan@gmail.com'],  # Send to yourself for testing
            fail_silently=False,
        )
        return HttpResponse("✅ Email sent successfully! Check your inbox.")
    except Exception as e:
        return HttpResponse(f"❌ Email failed: {str(e)}")