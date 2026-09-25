from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import StudentApplicationForm, StudentLoginForm, ResultLookupForm
from .models import StudentApplication, Result
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
    
    


   
def _student_required(view):
    """Only logged-in users with a student_profile."""
    @login_required(login_url='student_login')
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'student_profile'):
            messages.error(request, "This page is for students only.")
            return redirect('student_login')
        return view(request, *args, **kwargs)
    return wrapper


@require_http_methods(["GET", "POST"])
def student_login(request):
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        return redirect('student_dashboard')

    next_url = request.GET.get('next', request.POST.get('next', ''))

    if request.method == 'POST':
        form = StudentLoginForm(request.POST, request=request)
        if form.is_valid():
            user = form.user
            login(request, user)
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            messages.success(
                request,
                f"Welcome back, {user.first_name or user.username}!"
            )
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('student_dashboard')
    else:
        form = StudentLoginForm(request=request)

    return render(request, 'students/login.html', {'form': form, 'next': next_url})


def student_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('student_login')


@_student_required
def student_dashboard(request):
    profile = request.user.student_profile

    sessions = (Result.objects
                .filter(student=profile)
                .values_list('session', flat=True)
                .distinct()
                .order_by('-session'))

    session_filter = request.GET.get('session', '').strip()
    term_filter = request.GET.get('term', '').strip()

    qs = Result.objects.filter(student=profile).select_related('subject')
    if session_filter:
        qs = qs.filter(session=session_filter)
    if term_filter:
        qs = qs.filter(term=term_filter)

    results = list(qs)

    stats = {
        'count': len(results),
        'total': sum(r.total for r in results) if results else 0,
        'average': (sum(r.total for r in results) / len(results)) if results else 0,
    }

    lookup_form = ResultLookupForm(
        initial={'session': session_filter, 'term': term_filter},
        session_choices=list(sessions),
    )

    return render(request, 'students/dashboard.html', {
        'profile': profile,
        'results': results,
        'stats': stats,
        'sessions': sessions,
        'session_filter': session_filter,
        'term_filter': term_filter,
        'lookup_form': lookup_form,
    })


@_student_required
def check_result(request):
    profile = request.user.student_profile

    sessions = (Result.objects
                .filter(student=profile)
                .values_list('session', flat=True)
                .distinct()
                .order_by('-session'))

    session_filter = request.GET.get('session', '').strip()
    term_filter = request.GET.get('term', '').strip()

    qs = Result.objects.filter(student=profile).select_related('subject')
    if session_filter:
        qs = qs.filter(session=session_filter)
    if term_filter:
        qs = qs.filter(term=term_filter)

    results = list(qs)
    total_score = sum(r.total for r in results) if results else 0
    average = (total_score / len(results)) if results else 0

    if average >= 75:      overall_grade = 'A'
    elif average >= 65:    overall_grade = 'B'
    elif average >= 55:    overall_grade = 'C'
    elif average >= 45:    overall_grade = 'D'
    elif average >= 40:    overall_grade = 'E'
    else:                  overall_grade = 'F'

    lookup_form = ResultLookupForm(
        initial={'session': session_filter, 'term': term_filter},
        session_choices=list(sessions),
    )

    return render(request, 'students/check_result.html', {
        'profile': profile,
        'results': results,
        'total_score': total_score,
        'average': round(average, 2),
        'overall_grade': overall_grade,
        'lookup_form': lookup_form,
        'session_filter': session_filter,
        'term_filter': term_filter,
    })