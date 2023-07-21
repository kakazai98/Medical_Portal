from datetime import datetime, timedelta
from django.utils import timezone
from datetime import datetime
from random import randint, choice
from django.contrib.auth.models import User
from website.models import Patient, Provider, MedicalEncounter, Diagnosis, Procedure, Medication, LabResult, ImagingReport, VitalSign, Allergy

def create_sample_data():
    # Create a patient
    patient = Patient.objects.create(
        first_name='John',
        last_name='Doe',
        dob='1985-08-12',
        gender='Male',
        phone='555-123-4567',
        email='johndoe@example.com',
        address='123 Main St, Cityville',
        medical_history='Hypertension, diabetes',
    )

    User.objects.create_user(username=patient.email, password='123')
    
    #Create a Provider
    provider = Provider.objects.create(
        first_name='Dr. Sarah',
        last_name='Thompson',
        specialty='Cardiology',
        phone='9876543210',
        email='sarahthompson@example.com',
        address='111 Heart St, Cityville',
        organization='Cityville Cardiology',
    )

#-----------------------------  MedicalEncounter 1 -----------------------

    # Create a MedicalEncounter
    encounter = MedicalEncounter.objects.create(
        patient=patient,
        date_time=datetime.strptime('2023-05-17 10:30:00+00:00', '%Y-%m-%d %H:%M:%S%z'),
        provider=provider,
        chief_complaint='Chest pain',
    )

    # Create a Diagnosis
    diagnosis = Diagnosis.objects.create(
        patient=patient,
        date=encounter.date_time.date(),
        description='Coronary artery disease',
        code='I25.10',
    )
    encounter.diagnoses.add(diagnosis)

    # Create a Procedure
    procedure = Procedure.objects.create(
        patient=patient,
        date=encounter.date_time.date(),
        description='Cardiac catheterization',
        code='93458',
    )
    encounter.procedures.add(procedure)

    # Create a Medication
    medication = Medication.objects.create(
        medication_name=f'Lisinopril',
        dosage='10mg',
        frequency='Once daily',
        duration='Ongoing',
        instructions='Take 1 tablet daily with food',
    )
    encounter.medications.add(medication)
    patient.medications.add(medication)

    # Create LabResults
    lab_result = LabResult.objects.create(
        patient=patient,
        test_name='Cholesterol',
        test_date=encounter.date_time.date(),
        result_value='200 mg/dL',
        reference_range='<200 mg/dL',
    )
    encounter.lab_results.add(lab_result)

    # Create ImagingReports
    imaging_report = ImagingReport.objects.create(
        patient=patient,
        imaging_type='X-ray	',
        report_date=encounter.date_time.date(),
        findings='No abnormalities detected',
        impression='N/A',
    )
    encounter.imaging_reports.add(imaging_report)

    # Create VitalSigns
    vital_sign = VitalSign.objects.create(
        patient=patient,
        measurement_date=encounter.date_time.date(),
        systolic_blood_pressure=120,
        diastolic_blood_pressure=80,
        heart_rate=72,
        respiratory_rate=14,
        temperature=98.6,
    )
    encounter.vital_signs.add(vital_sign)

    vital_sign = VitalSign.objects.create(
        patient=patient,
        measurement_date=datetime.strptime('2023-05-19 09:15:00+00:00', '%Y-%m-%d %H:%M:%S%z'),
        systolic_blood_pressure=125,
        diastolic_blood_pressure=92,
        heart_rate=77,
        respiratory_rate=15,
        temperature=97.3,
    )
    encounter.vital_signs.add(vital_sign)

#-----------------------------  MedicalEncounter 2 -----------------------

    # Create a MedicalEncounter
    encounter = MedicalEncounter.objects.create(
        patient=patient,
        date_time=datetime.strptime('2023-05-22 09:15:00+00:00', '%Y-%m-%d %H:%M:%S%z'),
        provider=provider,
        chief_complaint='Shortness of breath',
    )

    # Create a Diagnosis
    diagnosis = Diagnosis.objects.create(
        patient=patient,
        date=encounter.date_time.date(),
        description='Chronic obstructive pulmonary disease',
        code='J44.9',
    )
    encounter.diagnoses.add(diagnosis)

    # Create a Procedure
    procedure = Procedure.objects.create(
        patient=patient,
        date=encounter.date_time.date(),
        description='Pulmonary function test',
        code='94010',
    )
    encounter.procedures.add(procedure)

    # Create a Medication
    medication = Medication.objects.create(
        medication_name='Albuterol Inhaler',
        dosage='2 puffs',
        frequency='As needed',
        duration='Permanent',
        instructions='Inhale 2 puffs when experiencing shortness of breath',
    )
    encounter.medications.add(medication)
    patient.medications.add(medication)

    # Create LabResults
    lab_result = LabResult.objects.create(
        patient=patient,
        test_name='Hemoglobin A1c',
        test_date=encounter.date_time.date(),
        result_value='7.2%	',
        reference_range=f"4.0%-5.6%",
    )
    encounter.lab_results.add(lab_result)

    # Create VitalSigns
    vital_sign = VitalSign.objects.create(
        patient=patient,
        measurement_date=encounter.date_time.date(),
        systolic_blood_pressure=135,
        diastolic_blood_pressure=95,
        heart_rate=85,
        respiratory_rate=20,
        temperature=101.0,
    )
    encounter.vital_signs.add(vital_sign)

    vital_sign = VitalSign.objects.create(
        patient=patient,
        measurement_date=datetime.strptime('2023-05-25 09:15:00+00:00', '%Y-%m-%d %H:%M:%S%z'),
        systolic_blood_pressure=120,
        diastolic_blood_pressure=90,
        heart_rate=80,
        respiratory_rate=16,
        temperature=98.3
    )
    encounter.vital_signs.add(vital_sign)

    patient = Patient.objects.create(
        first_name='Alice',
        last_name='Johnson',
        dob='1992-03-25',
        gender='Female',
        phone='555-987-6543',
        email='alicejohnson@example.com',
        address='456 Elm St, Townsville',
        medical_history='Asthma, allergies',
    )

    User.objects.create_user(username=patient.email, password='123')

    patient = Patient.objects.create(
        first_name='David',
        last_name='Smith',
        dob='1976-11-02',
        gender='Male',
        phone='555-555-5555',
        email='davidsmith@example.com',
        address='789 Oak St, Villageland',
    )

    User.objects.create_user(username=patient.email, password='123')

    

    provider = Provider.objects.create(
        first_name='Dr. Michael',
        last_name='Johnson',
        specialty='Dermatology',
        phone='555-222-3333',
        email='michaeljohnson@example.com',
        address='222 Skin Ave, Townsville',
        organization='Townsville Dermatology',
    )

    provider = Provider.objects.create(
        first_name='Dr. Emily',
        last_name='Davis',
        specialty='Orthopedics',
        phone='555-333-4444',
        email='emilydavis@example.com',
        address='333 Bone Dr, Villageland',
        organization='Villageland Orthopedics',
    )


create_sample_data()