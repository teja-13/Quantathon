import os
import shutil
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from patients.models import Patient
from diagnosis.models import Diagnosis
from reports.models import MedicalReport
from accounts.models import UserProfile
from system_settings.models import UserSettings
from services.api_client import ai_client, generate_report

class Command(BaseCommand):
    help = "Seed database with realistic medical patients, diagnoses, and reports."

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # 1. Create Default Users
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@oncovision.med',
                'first_name': 'System',
                'last_name': 'Administrator',
                'is_staff': True,
                'is_superuser': True
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()

        doctor_user, _ = User.objects.get_or_create(
            username='doctor',
            defaults={
                'email': 'dr.jenkins@oncovision.med',
                'first_name': 'Sarah',
                'last_name': 'Jenkins',
            }
        )
        doctor_user.set_password('password123')
        doctor_user.save()

        # Update profiles & settings
        profile, _ = UserProfile.objects.get_or_create(user=doctor_user)
        profile.title = 'Senior Medical Oncologist'
        profile.department = 'Department of Clinical Diagnostic Radiology'
        profile.phone = '+1 (555) 349-2041'
        profile.save()

        UserSettings.objects.get_or_create(user=doctor_user)
        UserSettings.objects.get_or_create(user=admin_user)

        # 2. Ensure media/scans directory exists
        media_scans_dir = settings.MEDIA_ROOT / 'scans'
        os.makedirs(media_scans_dir, exist_ok=True)

        # Copy static svg images to media/scans if available
        static_img_dir = settings.BASE_DIR / 'static' / 'images'
        sample_scan_files = {}
        for cancer_name, filename in [
            ('Brain Cancer', 'brain-cancer.svg'),
            ('Breast Cancer', 'breast-cancer.svg'),
            ('Lung Cancer', 'lung-cancer.svg'),
            ('Liver Cancer', 'liver-cancer.svg'),
            ('Kidney Cancer', 'kidney-cancer.svg'),
        ]:
            src = static_img_dir / filename
            dst = media_scans_dir / filename
            if os.path.exists(src):
                shutil.copy(src, dst)
                sample_scan_files[cancer_name] = f'scans/{filename}'
            else:
                sample_scan_files[cancer_name] = f'scans/{filename}'

        # Clear legacy diagnoses and reports with obsolete types
        MedicalReport.objects.all().delete()
        Diagnosis.objects.all().delete()

        # 3. Create Sample Patients
        patients_data = [
            {
                'first_name': 'Eleanor', 'last_name': 'Vance', 'age': 54, 'gender': 'Female',
                'blood_group': 'A+', 'phone': '+1 (555) 234-5678', 'email': 'eleanor.vance@example.com',
                'address': '742 Evergreen Terrace, Springfield', 'doctor_name': 'Dr. Sarah Jenkins',
                'notes': 'Presented with chronic headaches and vision blurry spells.'
            },
            {
                'first_name': 'Arthur', 'last_name': 'Pendelton', 'age': 62, 'gender': 'Male',
                'blood_group': 'O+', 'phone': '+1 (555) 876-5432', 'email': 'arthur.p@example.com',
                'address': '128 Elm Street, Boston, MA', 'doctor_name': 'Dr. Sarah Jenkins',
                'notes': 'Persistent smoker cough, 30 pack-year history.'
            },
            {
                'first_name': 'Sofia', 'last_name': 'Rodriguez', 'age': 46, 'gender': 'Female',
                'blood_group': 'B+', 'phone': '+1 (555) 432-1098', 'email': 'sofia.r@example.com',
                'address': '450 Sunset Blvd, Los Angeles, CA', 'doctor_name': 'Dr. Sarah Jenkins',
                'notes': 'Routine screening mammogram detected microcalcifications.'
            },
            {
                'first_name': 'Marcus', 'last_name': 'Thorne', 'age': 68, 'gender': 'Male',
                'blood_group': 'AB-', 'phone': '+1 (555) 654-9870', 'email': 'marcus.t@example.com',
                'address': '92 Oak Ridge Way, Chicago, IL', 'doctor_name': 'Dr. Sarah Jenkins',
                'notes': 'Abdominal discomfort, elevated serum AFP levels.'
            },
            {
                'first_name': 'Clara', 'last_name': 'Oswald', 'age': 39, 'gender': 'Female',
                'blood_group': 'O-', 'phone': '+1 (555) 321-7654', 'email': 'clara.o@example.com',
                'address': '15 Baker Street, Seattle, WA', 'doctor_name': 'Dr. Sarah Jenkins',
                'notes': 'Left flank abdominal pain and microscopic hematuria.'
            },
            {
                'first_name': 'David', 'last_name': 'Miller', 'age': 59, 'gender': 'Male',
                'blood_group': 'A-', 'phone': '+1 (555) 789-0123', 'email': 'david.m@example.com',
                'address': '304 Pinehurst Ave, Austin, TX', 'doctor_name': 'Dr. Sarah Jenkins',
                'notes': 'Sub-centimeter lung nodule observed during routine chest CT.'
            },
        ]

        created_patients = []
        for pdata in patients_data:
            patient, _ = Patient.objects.get_or_create(
                first_name=pdata['first_name'],
                last_name=pdata['last_name'],
                defaults={
                    'age': pdata['age'],
                    'gender': pdata['gender'],
                    'blood_group': pdata['blood_group'],
                    'phone': pdata['phone'],
                    'email': pdata['email'],
                    'address': pdata['address'],
                    'doctor_name': pdata['doctor_name'],
                    'medical_notes': pdata['notes'],
                }
            )
            created_patients.append(patient)

        # 4. Create Sample Diagnoses & Reports
        cancer_types_cycle = ['Brain Cancer', 'Breast Cancer', 'Lung Cancer', 'Liver Cancer', 'Kidney Cancer']
        
        for idx, patient in enumerate(created_patients):
            ctype = cancer_types_cycle[idx % len(cancer_types_cycle)]
            img_rel_path = sample_scan_files.get(ctype, 'scans/brain-cancer.svg')

            diag = Diagnosis.objects.create(
                patient=patient,
                cancer_type=ctype,
                medical_image=img_rel_path,
                prediction='Cancerous' if idx % 4 != 3 else 'Non-Cancerous',
                confidence=95.8 - (idx * 0.7),
                probability=0.958 - (idx * 0.007),
                processing_time=1.12 + (idx * 0.05),
                estimated_stage='Stage II (Localized)' if idx % 2 == 0 else 'Stage I (Early)',
                model_explanation=ai_client.CANCER_DESCRIPTIONS[ctype]['explanation'],
                status='Completed'
            )

            # Create corresponding report
            rep_payload = generate_report({'cancer_type': ctype, 'patient_name': patient.full_name})
            MedicalReport.objects.create(
                diagnosis=diag,
                report_number=f"REP-2026-{2000 + idx}",
                treatment_guidelines=rep_payload['treatment_guidelines'],
                doctor_notes=rep_payload['doctor_notes'],
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded database with users, patients, diagnoses, and reports!"))
