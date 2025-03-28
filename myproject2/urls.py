"""
URL configuration for myproject2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from doctors_appointment.views import *


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homefn),
    path('about/',aboutfn),
    path('services/',servicesfn),
    path('base/',basefn),
   
    

    path('book_app/',book_appointmentfn),
    path('editbooking/<int:appointment_id>',editbooking),
    path('deletebooking/<int:appointment_id>',deletebooking),
    path('patient_dashboard/',patientfn),
   
    path('loogg/',looogg),
    path('login/',loginfn),
    path('register/',registerfn),
    path('logout/',logoutfn),

    path('manage/',manage_appointments),
    path('approve/<int:appointment_id>', approve_appointment),
    path('cancel/<int:appointment_id>', cancel_appointment),
   
   
    path('doctor/',ourdoctorfn),
    path('dashboard/',doctor_dashboardfn),
    path('approve_update/<int:appointment_id>', approve_updatefn ),
    path('cancel_update/<int:appointment_id>', cancel_updatefn ),
  
   
    path('review/',review),
    path('blog/',blog),
    path('search/',search_appointments),

    path('free/',freecheckup),
    path('ambulance/',ambulance),
    path('medicine/',medicine),
    path('bedfacility/',bedfacility),
    path('totalcare/',totalcare),
    path('expertdr/',expertdr),

    path('api-appointment/',apiappointmentfn),
    path('api-doctor/',api_doctor_list),

    path('api-addappointment/',api_cr_appointment),
    path('api-edyappointment/<int:id>',api_fn_ed),
    path('api-deleteappointment/<int:id>',api_fn_dt),

    path('api-register/',apiregisterfn),
    path('api-login/',apiloginfn),


   

   

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
