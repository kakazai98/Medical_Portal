from django.urls import path

from website import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.patient_signup, name='signup'),
    path('login.html', views.login_view, name='login'),
    path('login.html', views.logout, name='logout'),

    path('home.html',views.dashboard,name='home'),
    path('patient_update.html',views.update_account, name='patient_update'),

    path('schedule.html',views.schedule_meeting,name='schedule'),
    path('delete_schedule.html',views.delete_schedule,name='delete_schedule'),

    path('allergies.html',views.allergies,name='allergies'),
    path('create_allergy.html',views.create_allergy,name='create_allergy'),
    path('delete_allergy.html',views.delete_allergy,name='delete_allergy'),

    path('insurance.html',views.insurance,name='insurance'),
    path('create_insurance.html',views.create_insurance,name='create_insurance'),
   
    path('compose_message_patient.html', views.compose_message_patient, name='compose_message_patient'),
    path('inbox_patient.html', views.inbox_patient, name='inbox_patient'),
    
    path('admin.html',views.admin,name='admin'),
    path('admin_patients.html',views.admin_patients,name='admin_patients'),
        
    path('admin_add_provider.html',views.admin_add_provider,name='admin_add_provider'),

    path('admin_medications.html',views.admin_medications,name='admin_medications'),
    path('admin_add_medication.html',views.admin_add_medication,name='admin_add_medication'),
    path('admin_create_medication.html',views.admin_create_medication,name='admin_create_medication'),

    path('vital_patient.html',views.display_vitals,name='vital_patient')
]


