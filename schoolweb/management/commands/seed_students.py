from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from schoolweb.models import StudentProfile, Subject, Result


class Command(BaseCommand):
    help = "Create a test student and sample results."

    def handle(self, *args, **opts):
        subj_names = [
            ('Mathematics', 'MTH'),
            ('English Language', 'ENG'),
            ('Basic Science', 'BSC'),
            ('Social Studies', 'SOS'),
            ('Computer Studies', 'CMP'),
        ]
        subjects = []
        for name, code in subj_names:
            s, _ = Subject.objects.get_or_create(name=name, code=code)
            subjects.append(s)

        user, created = User.objects.get_or_create(
            username='student001',
            defaults={
                'first_name': 'Ada',
                'last_name': 'Nwosu',
                'email': 'ada.nwosu@student.newheaven.edu',
            },
        )
        if created:
            user.set_password('student123')
            user.save()
            self.stdout.write(self.style.SUCCESS("Created user 'student001'"))

        profile, _ = StudentProfile.objects.get_or_create(
            user=user,
            defaults={
                'admission_number': 'NH/2026/001',
                'student_class': 'JSS1',
                'gender': 'F',
                'guardian_name': 'Mr. Emeka Nwosu',
                'guardian_phone': '+234 800 000 0000',
            },
        )

        scores = [
            (subjects[0], '1st', '2025/2026', 32, 55),
            (subjects[1], '1st', '2025/2026', 28, 48),
            (subjects[2], '1st', '2025/2026', 25, 40),
            (subjects[3], '1st', '2025/2026', 22, 38),
            (subjects[4], '1st', '2025/2026', 30, 52),
        ]
        for subj, term, session, ca, ex in scores:
            Result.objects.update_or_create(
                student=profile, subject=subj, term=term, session=session,
                defaults={'ca_score': ca, 'exam_score': ex},
            )

        self.stdout.write(self.style.SUCCESS("Seeded student + results."))
        self.stdout.write("Login at /students/login/ with:")
        self.stdout.write("  Admission No: NH/2026/001")
        self.stdout.write("  Password:     student123")