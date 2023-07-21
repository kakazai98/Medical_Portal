from django.db import models

class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True, db_column='Patient_ID')
    first_name = models.CharField(max_length=100, db_column='First_Name')
    last_name = models.CharField(max_length=100, db_column='Last_Name')
    dob = models.DateField(db_column='DOB')
    gender = models.CharField(max_length=10, db_column='Gender')
    phone = models.CharField(max_length=20, db_column='Phone')
    email = models.EmailField(max_length=100, db_column='Email')
    address = models.CharField(max_length=200, db_column='Address')
    insurance_info = models.OneToOneField('Insurance', on_delete=models.CASCADE, db_column='Insurance_ID', related_name='patients', null=True)
    medical_history = models.TextField(db_column='Medical_History', null=True)
    allergies = models.ManyToManyField('Allergy', db_column='Allergy', related_name='patients', null=True)
    medications = models.ManyToManyField('Medication', db_column='Medication', related_name='patients', null=True)
    
    def __str__(self):
        return f'{self.email}'
    
class MedicalEncounter(models.Model):
    encounter_id = models.AutoField(primary_key=True, db_column='Encounter_ID')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, db_column='Patient_ID', related_name='medical_encounters')
    date_time = models.DateTimeField(db_column='DateTime')
    provider = models.ForeignKey('Provider', on_delete=models.CASCADE, db_column='Provider_ID', related_name='medical_encounters')
    chief_complaint = models.CharField(max_length=200, db_column='Chief_Complaint')
    diagnoses = models.ManyToManyField('Diagnosis', db_column='Diagnosis_ID', related_name='medical_encounters')
    procedures = models.ManyToManyField('Procedure', db_column='Procedure_ID', related_name='medical_encounters')
    medications = models.ManyToManyField('Medication', db_column='Medication_ID', related_name='medical_encounters')
    lab_results = models.ManyToManyField('LabResult', db_column='Results_ID', related_name='medical_encounters')
    imaging_reports = models.ManyToManyField('ImagingReport', db_column='Report_ID', related_name='medical_encounters')
    vital_signs = models.ManyToManyField('VitalSign', db_column='Vital_Sign_ID', related_name='medical_encounters')

    def __str__(self):
        return f'Meeting with {self.provider} on {self.date_time}'

class LabResult(models.Model):
    results_id = models.AutoField(primary_key=True, db_column='Results_ID')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, db_column='Patient_ID', related_name='lab_results')
    test_name = models.CharField(max_length=100, db_column='Test_Name')
    test_date = models.DateField(db_column='Test_Date')
    result_value = models.CharField(max_length=100, db_column='Result_Value')
    reference_range = models.CharField(max_length=100, db_column='Reference_Range')


class ImagingReport(models.Model):
    report_id = models.AutoField(primary_key=True, db_column='Report_ID')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, db_column='Patient_ID', related_name='imaging_reports')
    imaging_type = models.CharField(max_length=100, db_column='Imaging_Type')
    report_date = models.DateField(db_column='Report_Date')
    findings = models.TextField(db_column='Findings')
    impression = models.TextField(db_column='Impression')

class Insurance(models.Model):
    insurance_id = models.AutoField(primary_key=True, db_column='Insurance_ID')
    insurance_provider_name = models.CharField(max_length=100, db_column='Insurance_Provider_Name')
    policy_number = models.CharField(max_length=100, db_column='Policy_Number')
    coverage_details = models.TextField(db_column='Coverage_Details')

    def __str__(self):
        return f'{self.insurance_provider_name} - {self.policy_number}'

class Provider(models.Model):
    provider_id = models.AutoField(primary_key=True, db_column='Provider_ID')
    first_name = models.CharField(max_length=100, db_column='First_Name')
    last_name = models.CharField(max_length=100, db_column='Last_Name')
    specialty = models.CharField(max_length=100, db_column='Specialty')
    phone = models.CharField(max_length=20, db_column='Phone')
    email = models.EmailField(max_length=100, db_column='Email')
    address = models.CharField(max_length=200, db_column='Address')
    organization = models.CharField(max_length=100, db_column='Organization')

    def __str__(self):
        return f'{self.first_name} {self.last_name} , {self.specialty}'

class Medication(models.Model):
    medication_id = models.AutoField(primary_key=True, db_column='Medication_ID')
    medication_name = models.CharField(max_length=100, db_column='Medication_Name')
    dosage = models.CharField(max_length=100, db_column='Dosage')
    frequency = models.CharField(max_length=100, db_column='Frequency')
    duration = models.CharField(max_length=100, db_column='Duration')
    instructions = models.TextField(db_column='Instructions')

    def __str__(self):
        return f'{self.medication_name} - {self.dosage} - {self.frequency} - {self.duration}'

class VitalSign(models.Model):
    vital_sign_id = models.AutoField(primary_key=True, db_column='Vital_Sign_ID')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, db_column='Patient_ID', related_name='vital_signs')
    measurement_date = models.DateField(db_column='Measurement_Date')
    systolic_blood_pressure = models.IntegerField(db_column='Systolic_Blood_Pressure')
    diastolic_blood_pressure = models.IntegerField(db_column='Diastolic_Blood_Pressure')
    heart_rate = models.IntegerField(db_column='Heart_Rate')
    respiratory_rate = models.IntegerField(db_column='Respiratory_Rate')
    temperature = models.DecimalField(max_digits=4, decimal_places=1, db_column='Temperature')

class Allergy(models.Model):
    allergy_id = models.AutoField(primary_key=True, db_column='Allergy_ID')
    allergen = models.CharField(max_length=100, db_column='Allergen')
    reaction = models.CharField(max_length=100, db_column='Reaction')
    severity = models.CharField(max_length=100, db_column='Severity')

    def __str__(self):
        return f'{self.allergen} - {self.reaction} - {self.severity}'

class Patient_Message(models.Model):
    message_id = models.AutoField(primary_key=True, db_column='Message_ID')
    sender = models.ForeignKey('Patient', on_delete=models.CASCADE, db_column='Sender_ID', related_name='sent_messages')
    receiver = models.ForeignKey('Provider', on_delete=models.CASCADE, db_column='Receiver_ID', related_name='received_messages')
    subject = models.CharField(max_length=100, db_column='Subject')
    content = models.TextField(db_column='Content')
    datetime = models.DateTimeField(db_column='DateTime')

class Diagnosis(models.Model):
    diagnosis_id = models.AutoField(primary_key=True, db_column='Diagnosis_ID')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, db_column='Patient_ID', related_name='diagnoses')
    date = models.DateField(db_column='Date')
    description = models.TextField(db_column='Description')
    code = models.CharField(max_length=100, db_column='Code')

class Procedure(models.Model):
    procedure_id = models.AutoField(primary_key=True, db_column='Procedure_ID')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, db_column='Patient_ID', related_name='procedures')
    date = models.DateField(db_column='Date')
    description = models.TextField(db_column='Description')
    code = models.CharField(max_length=100, db_column='Code')

class User(models.Model):
    user_id = models.AutoField(primary_key=True, db_column='User_ID')
    username = models.CharField(max_length=100, db_column='Username')
    password = models.CharField(max_length=100, db_column='Password')
    role = models.CharField(max_length=100, db_column='Role')


