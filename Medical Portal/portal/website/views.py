from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from .dataforms import PatientSignUpForm, LoginForm, AllergyForm, MessageForm, ProviderForm, InsuranceForm
from .dataforms import PatientMedicationForm, MedicationForm, MeetingForm,ScheduleDelete, PatientUpdateForm, AllergyDelete


from .models import Patient, Provider, Allergy, MedicalEncounter, Medication, Patient_Message, Procedure, VitalSign, LabResult, ImagingReport, Diagnosis


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import base64

#---------------------------------------------------------------------------------
#--------------------------- Signup ----------------------------------------------
#---------------------------------------------------------------------------------

def patient_signup(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_user(username='admin', password='admin')
        print('Admin user created successfully.')
    else:
        print('Admin user already exists.')
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            message = None
            # Extract form data
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create a new user account
            if User.objects.filter(username=username).exists():
                message = "Username already exists."
            else:
                user = User.objects.create_user(username=username, password=password)

                # Create a patient profile for the user
                patient = Patient(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    dob=form.cleaned_data['date_of_birth'],
                    gender=form.cleaned_data['gender'],
                    phone=form.cleaned_data['phone'],
                    email=form.cleaned_data['email'],
                    address=form.cleaned_data['address'],
                )

                # Save the patient profile
                patient.save()

            form = PatientSignUpForm()
            return render(request, 'patient_signup.html', {'form': form, 'message':message})  
    else:
        form = PatientSignUpForm()

    return render(request, 'patient_signup.html', {'form': form})


#---------------------------------------------------------------------------------
#--------------------------- Login and Logout ------------------------------------
#---------------------------------------------------------------------------------


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        request.session['user'] = ''
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['user'] = user.username
                request.session['is_logged_in'] = True
                if username=='admin':
                    return HttpResponseRedirect ('admin.html')
                else:
                    return HttpResponseRedirect ('home.html') 

            else:
                message = "Invalid username or password."
        else:
            message = "Invalid form submission."
    else:
        form = LoginForm()
        message = None
        request.session['is_logged_in'] = False
    context = {
        'form': form,
        'message': message,
    }
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    request.session['user'] = ''
    return HttpResponseRedirect ('login.html') 


#---------------------------------------------------------------------------------
#--------------------------- Patient Account -----------------------------------
#---------------------------------------------------------------------------------

@login_required
def dashboard(request):
    if request.session['is_logged_in']==True:
        if request.session['user']!='admin':
            output = Patient.objects.filter(email=request.session['user'])
            print(output)
            form = PatientUpdateForm()
            return render(request, 'home.html',{'out':output,'form':form})
    return HttpResponseRedirect ('login.html')
    

@login_required
def update_account(request):
    patient = Patient.objects.get(email=request.session['user'])

    if request.method == 'POST':
        form = PatientUpdateForm(request.POST)
        if form.is_valid():
            patient.first_name = form.cleaned_data['first_name'] or patient.first_name
            patient.last_name = form.cleaned_data['last_name'] or patient.last_name
            patient.dob = form.cleaned_data['dob'] or patient.dob
            patient.gender = form.cleaned_data['gender'] or patient.gender
            patient.phone = form.cleaned_data['phone'] or patient.phone
            patient.email = form.cleaned_data['email'] or patient.email
            patient.address = form.cleaned_data['address'] or patient.address

            patient.save()
    return HttpResponseRedirect('home.html')

#---------------------------------------------------------------------------------
#--------------------------- Patient Allergy -------------------------------------
#---------------------------------------------------------------------------------


@login_required
def allergies(request):
    if request.session['is_logged_in']==True:
        if request.session['user']!='admin':
            form1 = AllergyForm()
            form2 = AllergyDelete(request.session['user'])
            return render(request, 'allergies.html',{"form1":form1,"form2":form2})
    return HttpResponseRedirect ('login.html')

@login_required
def create_allergy(request):
    patient = Patient.objects.get(email=request.session['user'])
    if request.method == 'POST':
        form = AllergyForm(request.POST)
        if form.is_valid():
            allergy = form.save()
            if allergy not in patient.allergies.all(): 
                patient.allergies.add(allergy)
            else:
                print('This allergy is already associated with the patient.')
    return HttpResponseRedirect ('allergies.html')

def delete_allergy(request):
    email = request.session['user']
    patient = Patient.objects.get(email=email)

    if request.method == 'POST':
        form = AllergyDelete(email, request.POST)
        if form.is_valid():
            selected_allergy = form.cleaned_data['allergy']
            patient = Patient.objects.get(email=email)
            patient.allergies.remove(selected_allergy)
            selected_allergy.delete()
    return HttpResponseRedirect ('allergies.html')



#---------------------------------------------------------------------------------
#--------------------------- Patient Insurance -----------------------------------
#---------------------------------------------------------------------------------

@login_required
def insurance(request):
    if request.session['is_logged_in']==True:
        if request.session['user']!='admin':
            form1 = InsuranceForm()
            return render(request, 'insurance.html',{"form1":form1})
    return HttpResponseRedirect ('login.html')

@login_required
def create_insurance(request):
    email = request.session['user']
    patient = Patient.objects.get(email=email)  
    if request.method == 'POST':
        form = InsuranceForm(request.POST)
        if form.is_valid():
            insurance = form.save()
            patient.insurance_info = insurance
            patient.save()
    return HttpResponseRedirect ('insurance.html')

#---------------------------------------------------------------------------------
#--------------------------- Patient Schedule ------------------------------------
#---------------------------------------------------------------------------------

@login_required
def schedule_meeting(request):
    if request.session['is_logged_in']==True:
        if request.session['user']!='admin':
            email = request.session['user']
            patient = Patient.objects.get(email=email)
            out = MedicalEncounter.objects.filter(patient=patient)
            form2 = ScheduleDelete(email)
            if request.method == 'POST':
                form = MeetingForm(request.POST)
                if form.is_valid():
                    encounter = form.save(commit=False)
                    encounter.patient = patient
                    encounter.save()
                    form = MeetingForm()
                    return render(request, 'schedule.html', {'out':out,'form':form,'form2':form2})
            else:
                form = MeetingForm()
            return render(request, 'schedule.html', {'out':out,'form':form,'form2':form2})
    return HttpResponseRedirect ('login.html')

@login_required
def delete_schedule(request):
    if request.method == 'POST':
        email = request.session['user']
        form = ScheduleDelete(email, request.POST)
        if form.is_valid():
            selected_schedule = form.cleaned_data['schedule']
            current_datetime = timezone.now()

            if selected_schedule.date_time >= current_datetime:
                print(selected_schedule.date_time)
                print(current_datetime)
                selected_schedule.delete()

    return HttpResponseRedirect ('schedule.html')

#---------------------------------------------------------------------------------
#--------------------------- Communications --------------------------------------
#---------------------------------------------------------------------------------


@login_required
def compose_message_patient(request):
    if request.session['is_logged_in']==True:
        if request.session['user']!='admin':
            email = request.session['user']
            patient = Patient.objects.get(email=email)
            if request.method == 'POST':
                form = MessageForm(request.POST)
                if form.is_valid():
                    message = form.save(commit=False)
                    message.sender = patient
                    message.datetime = timezone.now()
                    message.save()
                    return HttpResponseRedirect ('inbox_patient.html')
            else:
                form = MessageForm()
            return render(request, 'compose_message_patient.html', {'form': form})
    return HttpResponseRedirect ('login.html')

@login_required
def inbox_patient(request):
    if request.session['is_logged_in']==True:
        if request.session['user']!='admin':
            email = request.session['user']
            patient = Patient.objects.get(email=email)
            received_messages = None
            sent_messages = Patient_Message.objects.filter(sender=patient)
            return render(request, 'inbox_patient.html', {'messages': received_messages,'messages_sent': sent_messages})
    return HttpResponseRedirect ('login.html')

@login_required
def message_details(request, message_id):
    if request.session['is_logged_in']==True:
        if request.session['user']!='admin':
            message = get_list_or_404(Patient_Message, pk=message_id)
            return render(request, 'message_details.html', {'message': message})
    return HttpResponseRedirect ('login.html')

#---------------------------------------------------------------------------------
#--------------------------- Admin Provider --------------------------------------
#---------------------------------------------------------------------------------



@login_required
def admin(request):
    if request.session['is_logged_in']==True:
        if request.session['user']=='admin':
            output = Provider.objects.all()
            form = ProviderForm()
            return render(request, 'admin.html',{"out":output,"form":form})
    return HttpResponseRedirect ('login.html')
    
@login_required
def admin_patients(request):
    if request.session['is_logged_in']==True:
        if request.session['user']=='admin':
            output = Patient.objects.all()
            return render(request, 'admin_patients.html',{"out":output})
    return HttpResponseRedirect ('login.html')



@login_required
def admin_add_provider(request):
    if request.method == 'POST':
        form = ProviderForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('admin.html')
    return HttpResponseRedirect ('admin.html')


#---------------------------------------------------------------------------------
#--------------------------- Admin Medication ------------------------------------
#---------------------------------------------------------------------------------


@login_required
def admin_medications(request):
    if request.session['is_logged_in']==True:
        if request.session['user']=='admin':
            form1 = MedicationForm()
            form2 = PatientMedicationForm()
            return render(request, 'admin_medications.html',{"form1":form1,"form2":form2})
    return HttpResponseRedirect ('login.html')

@login_required
def admin_create_medication(request):
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medication = form.save()  
    return HttpResponseRedirect ('admin_medications.html')

@login_required
def admin_add_medication(request):
    if request.method == 'POST':
        form = PatientMedicationForm(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            medication = form.cleaned_data['medication']
            if medication not in patient.medications.all(): 
                patient.medications.add(medication)
            else:
                print('This Medication is already associated with the patient.')
    return HttpResponseRedirect ('admin_medications.html')




def display_vitals(request):
    if request.session['is_logged_in']==True:
        if request.session['user']!='admin':
            email = request.session['user']
            patient = Patient.objects.get(email=email)
            
            # Retrieve all medical encounters related to the patient
            medical_encounters = MedicalEncounter.objects.filter(patient=patient)

            # Retrieve the vital sign data for each medical encounter
            vitals = []
            for encounter in medical_encounters:
                vitals.extend(encounter.vital_signs.all())

            # Extract the necessary data from the vital sign objects
            dates = [vital.measurement_date for vital in vitals]
            systolic_blood_pressure = [vital.systolic_blood_pressure for vital in vitals]
            diastolic_blood_pressure = [vital.diastolic_blood_pressure for vital in vitals]
            heart_rate = [vital.heart_rate for vital in vitals]
            respiratory_rate = [vital.respiratory_rate for vital in vitals]
            temperature = [vital.temperature for vital in vitals]

            # Create subplots for each vital sign
            fig, axs = plt.subplots(2, 2, figsize=(10, 8))
            fig.suptitle('Patient Vital Signs')

            # Plot the vital sign data in separate subplots
            axs[0, 0].bar( dates,systolic_blood_pressure,  label='Systolic Blood Pressure')
            axs[0, 0].bar( dates,diastolic_blood_pressure,  label='Diastolic Blood Pressure')
            axs[0, 1].bar( dates,heart_rate, label='Heart Rate')
            axs[1, 0].bar( dates,respiratory_rate,  label='Respiratory Rate')
            axs[1, 1].bar( dates,temperature, label='Temperature')

            # Rotate the x-axis tick labels by 45 degrees
            for ax in axs.flat:
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

            # Set labels and legends for each subplot
            axs[0, 0].set(xlabel='Date', ylabel='Blood Pressure (mmHg)')
            axs[0, 0].legend()
            axs[0, 1].set(xlabel='Date', ylabel='Heart Rate (bmp)')
            axs[0, 1].legend()
            axs[1, 0].set(xlabel='Date', ylabel='Respiratory Rate (breaths per minute)')
            axs[1, 0].legend()
            axs[1, 1].set(xlabel='Date', ylabel='Temperature °F')
            axs[1, 1].legend()


            # Adjust spacing between subplots
            plt.tight_layout()

            # Save the plot to a BytesIO object
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            # Encode the plot image as base64
            plot_data = base64.b64encode(buffer.read()).decode('utf-8')

            # Pass the plot data to the template context
            context = {
                'plot_data': plot_data,
            }

            # Render the template with the context
            return render(request, 'vital_patient.html', context) 
        
    return HttpResponseRedirect ('login.html')