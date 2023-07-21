from django import forms
from tempus_dominus.widgets import DatePicker
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Patient, Allergy, Provider, Medication, Insurance, LabResult, Diagnosis, Procedure, ImagingReport, MedicalEncounter, Patient_Message, VitalSign


class PatientSignUpForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    date_of_birth = forms.DateField(label='Date of Birth', widget=DatePicker())
    gender = forms.ChoiceField(label='Gender', choices=[('M', 'Male'), ('F', 'Female')])
    phone = forms.CharField(label='Phone', max_length=100)
    email = forms.EmailField(label='Email')
    address = forms.CharField(label='Address', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput)

#------------- Allergies -----------------------------

class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = ['allergen', 'reaction', 'severity']

class AllergyDelete(forms.Form):
    def __init__(self, patient_email, *args, **kwargs):
        super(AllergyDelete, self).__init__(*args, **kwargs)
        patient = Patient.objects.get(email=patient_email)
        allergies = patient.allergies.all()
        self.fields['allergy'] = forms.ModelChoiceField(queryset=allergies)

#------------- Provider Accounts -----------------------------

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = '__all__'

#------------- Medications -----------------------------

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['medication_name', 'dosage', 'frequency', 'duration', 'instructions']

class PatientMedicationForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), label='Patient')
    medication = forms.ModelChoiceField(queryset=Medication.objects.all(), label='Medication')


#------------- Insurance -----------------------------

class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = ['insurance_provider_name', 'policy_number', 'coverage_details']


#------------- Patient Update -----------------------------


class PatientUpdateForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    dob = forms.DateField(required=False)
    gender = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    address = forms.CharField(required=False)


#------------- Patient Schedule -----------------------------

class MeetingForm(forms.ModelForm):
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = MedicalEncounter
        fields = ['provider', 'date_time','chief_complaint']

    def clean_date_time(self):
        date_time = self.cleaned_data['date_time']
        provider = self.cleaned_data['provider']

        # Check if provider has any meetings within the next 30 minutes
        min_date_time = date_time - timezone.timedelta(minutes=29)
        max_date_time = date_time + timezone.timedelta(minutes=29)
        conflicting_meetings = MedicalEncounter.objects.filter(provider=provider, date_time__range=(min_date_time, max_date_time))

        if conflicting_meetings.exists():
            raise ValidationError('The selected provider is not available at the chosen date and time.')

        return date_time
    
class ScheduleDelete(forms.Form):
    def __init__(self, patient_email, *args, **kwargs):
        super(ScheduleDelete, self).__init__(*args, **kwargs)
        patient = Patient.objects.get(email=patient_email)
        schedule = MedicalEncounter.objects.filter(patient=patient).order_by('date_time')
        self.fields['schedule'] = forms.ModelChoiceField(queryset=schedule)

    
class MessageForm(forms.ModelForm):
    class Meta:
        model = Patient_Message
        fields = ['receiver', 'subject', 'content']
