import random
from faker import Faker
from datetime import datetime


from website.models import Patient, MedicalEncounter, LabResult, ImagingReport, Insurance, Provider, Medication, VitalSign, Allergy, Diagnosis, Procedure
from django.contrib.auth.models import User

# Generate sample data for the Allergy class
def generate_fake_data():
    
    fake = Faker()

    print('start')
    for _ in range(1000):
        allergy = Allergy.objects.create(
            allergy_id= fake.unique.random_number(digits=8),
            allergen= fake.word(),
            reaction= fake.sentence(),
            severity= random.choice(['Mild', 'Moderate', 'Severe']),
        )

    # Generate sample data for the Medication class

    for _ in range(1000):
        medication = Medication.objects.create(
            medication_id = fake.unique.random_number(digits=8),
            medication_name =  fake.word(),
            dosage = fake.word(),
            frequency = fake.word(),
            duration = fake.word(),
            instructions = fake.sentence(),
        )
        
    # Generate sample data for the Insurance class

    for _ in range(1000):
        insurance = Insurance.objects.create(
            insurance_id = fake.unique.random_number(digits=8),
            insurance_provider_name = fake.word(),
            policy_number = fake.word(),
            coverage_details = fake.sentence(),
        )

        patient = Patient.objects.create(
            patient_id = fake.unique.random_number(digits=8),
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            dob = fake.date_of_birth(),
            gender = random.choice(['Male', 'Female']),
            phone = fake.phone_number(),
            email = fake.email(),
            address = fake.address(),
            medical_history = fake.paragraph(),
        )
        # Generate sample data for allergies
        num_allergies = random.randint(0, 5)
        for _ in range(num_allergies):
            allergy = random.choice(Allergy.objects.all())
            patient.allergies.add(allergy)

        # Generate sample data for medications
        num_medications = random.randint(0, 5)
        for _ in range(num_medications):
            medication = random.choice(Medication.objects.all())
            patient.medications.add(medication)

        patient.insurance_info = insurance
        patient.save()

    print('Patients Done')

def generate_fake_data2():
    fake = Faker()
    # Generate sample data for LabResult class
    for _ in range(1000):
        patient = random.choice(Patient.objects.all())
        date_time = fake.date_time_this_year()
        date=date_time.date()

        lab_result = LabResult.objects.create(
            results_id=fake.unique.random_number(digits=8),
            patient=patient,
            test_name=fake.word(),
            test_date=date,
            result_value=fake.word(),
            reference_range=fake.word(),
        )

        # Generate sample data for ImagingReport class
        imaging_report = ImagingReport.objects.create(
            report_id=fake.unique.random_number(digits=8),
            patient=patient,
            imaging_type=fake.word(),
            report_date=date,
            findings=fake.paragraph(),
            impression=fake.paragraph(),
        )

        # Generate sample data for Provider class
        provider = Provider.objects.create(
            provider_id=fake.unique.random_number(digits=8),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            specialty=fake.word(),
            phone=fake.phone_number(),
            email=fake.email(),
            address=fake.address(),
            organization=fake.company(),
        )

        # Generate sample data for VitalSign class
        vital_sign = VitalSign.objects.create(
            vital_sign_id=fake.unique.random_number(digits=8),
            patient=patient,
            measurement_date=date,
            systolic_blood_pressure=random.randint(80, 140),
            diastolic_blood_pressure=random.randint(50, 90),
            heart_rate=random.randint(60, 100),
            respiratory_rate=random.randint(12, 20),
            temperature=round(random.uniform(94.0, 104.0), 1),
        )

        # Generate sample data for Diagnosis class
        diagnosis = Diagnosis.objects.create(
            diagnosis_id=fake.unique.random_number(digits=8),
            patient=patient,
            date=date,
            description=fake.paragraph(),
            code=fake.word(),
        )

        # Generate sample data for Procedure class
        procedure = Procedure.objects.create(
            procedure_id=fake.unique.random_number(digits=8),
            patient=patient,
            date=date,
            description=fake.paragraph(),
            code=fake.word(),
        )

        medical_encounter = MedicalEncounter.objects.create(
            encounter_id=fake.unique.random_number(digits=8),
            patient=patient,
            date_time=date_time,
            provider = random.choice(Provider.objects.all()),
            chief_complaint=fake.sentence(),
        )

        medical_encounter.diagnoses.add(diagnosis)
        medical_encounter.procedures.add(procedure)
        medical_encounter.lab_results.add(lab_result)
        medical_encounter.imaging_reports.add(imaging_report)
        medical_encounter.vital_signs.add(vital_sign)

        # Generate sample data for medications
        num_medications = random.randint(0, 3)
        for _ in range(num_medications):
            medication = random.choice(Medication.objects.all())
            patient.medications.add(medication)

generate_fake_data2()