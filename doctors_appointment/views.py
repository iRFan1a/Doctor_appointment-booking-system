from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse



from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from .models import Doctor, Appointment,Profile
from .forms import AppointmentForm
from django.contrib import messages



from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import Appointmentserializer,Doctorserializer,userserializer 





# Create your views here.


def homefn(request):
    
    return render(request,'home.html')



def basefn(request):
    
    return render(request,'base.html')

def servicesfn(request):
 
        return render(request,'services.html')

def registerfn(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['psw2']
        role = request.POST['role']

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'register.html', {'er': 'Passwords do not match!'})

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'er': 'Username already taken!'})

       

        # Create User & Profile
        user = User.objects.create_user(username=username,email=email, password=password)  

        Profile.objects.create(user=user, role=role)  

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('/loogg') 
    return render(request, 'register.html')



def loginfn(request):

    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user =auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)

            if user.is_superuser:
                return redirect('/manage')

           
            profile = Profile.objects.get(user=user)
           

            
            if profile.role == 'doctor':
                return redirect('/dashboard') 
            else:
                return redirect('/book_app') 
        else:
            return render(request, 'login.html', {'er': 'Invalid username or password!'})

    return render(request, 'login.html')
   

def logoutfn(request):
    auth.logout(request)
    return redirect('/loogg')
    
   


def aboutfn(request):
    
    return render(request,'about.html')

def ourdoctorfn(request):
    
    doctor = Doctor.objects.all()
   
    return render(request,'doctor_list.html',{'doctors': doctor})




@login_required(login_url='/login')
def book_appointmentfn(request):
  
    if request.method=='POST':
        f=AppointmentForm(request.POST,request.FILES)
        if f.is_valid():
            x=f.save(commit=False)
            x.us=request.user
            f.save()
            
            messages.success(request, "Your appointment has been booked successfully!") 
            return redirect('/book_app')
          
    else:

        f=AppointmentForm()
        return render(request,'book_appointment.html',{'form':f})
        

@login_required
def manage_appointments(request):
    appointments = Appointment.objects.select_related('doctor', 'patient').all()
    return render(request, 'admin.html', {'appointments': appointments})

@login_required
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'approved'
    appointment.save()
    return redirect('/manage')

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'canceled'
    appointment.save()
    return redirect('/manage')



@login_required
def doctor_dashboardfn(request):
    if request.user.profile.role != "doctor":
        return redirect('/dashboard')
    appointments = Appointment.objects.filter(doctor=request.user).order_by('-is_emergency', 'date')
    return render(request, 'doctor_dashboard.html', {'appointments': appointments})


def approve_updatefn(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = "approved"
    appointment.save()
    return redirect('/dashboard')  

def cancel_updatefn(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = "cancelled"
    appointment.save()
    return redirect('/dashboard')


def patientfn(request):
    # appointments = Appointment.objects.select_related('doctor', 'patient').all()
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request,'patient_dashboard.html', {'appointments': appointments})

   
def editbooking(request,appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
   
    if appointment.patient != request.user:
        return HttpResponse( "You are not allowed to edit this appointment.")
        return redirect('/patient_dashboard')

    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment successfully edited!")
            return redirect('/patient_dashboard')  
            
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, "book_appointment.html", {"form": form, "appointment": "edit appointment"})


def deletebooking(request,appointment_id):

    appointment=get_object_or_404(Appointment,id=appointment_id)
    if appointment.patient != request.user:
        return HttpResponse( "You are not allowed to delete this appointment.")
        return redirect('/patient_dashboard')
    if request.method=='POST':
     
        appointment.delete()
        messages.success(request, "Appointment successfully deleted!")
        return redirect('/patient_dashboard') 
   
    else:
    
        return render(request,'deletebooking.html', {'appointment': appointment})

def looogg(request):
    return render(request,'looogg.html')

def review(request):
    return render(request,'home.html')

def blog(request):
    return render(request,'home.html')


def freecheckup(request):
    return render(request,'free.html')
def ambulance(request):
    return render(request,'ambulance.html')
def medicine(request):
    return render(request,'medicine.html')
def bedfacility(request):
    return render(request,'bedfacility.html')
def totalcare(request):
    return render(request,'totalcare.html')
def expertdr(request):
    return render(request,'expertdr.html')



def search_appointments(request):
    query = request.GET.get('q')
   
    if query:
        results = Appointment.objects.filter(patient_name__icontains=query)  
      
    else:
        results = Appointment.objects.filter(patient=request.user) 

    return render(request, 'patient_dashboard.html', {'appointments': results, 'query': query})



@api_view(['GET'])
def apiappointmentfn(request):
    x=Appointment.objects.all()
    a=Appointmentserializer(x,many=True)
    return Response(a.data)


@api_view(['GET'])
def api_doctor_list(request):
    x=Doctor.objects.all()
    a=Doctorserializer(x,many=True)
    return Response(a.data)

@api_view(['POST'])
def api_cr_appointment(request):
        
        s = Appointmentserializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data)


@api_view(['PUT'])
def api_fn_ed(request,id):

        p=Appointment.objects.get(id=id)

        s = Appointmentserializer(data=request.data,instance=p, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data)
        
        return Response(s.errors)

@api_view(['DELETE'])
def api_fn_dt(request,id):

        p=Appointment.objects.get(id=id)
        p.delete()
        return Response("Done")


@api_view(['POST'])
def apiregisterfn(request):
    
    x = userserializer(data=request.data)

    
    if x.is_valid():

        u= x.save()
        u.set_password(request.data['password'])
        u.save()
       
           
        token,created = Token.objects.get_or_create(user=u)
        return Response({"token": token.key, "user":x.data},status=status.HTTP_201_CREATED)

    return Response(x.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def apiloginfn(request):

    user = get_object_or_404(User,username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail":"Not found."},status=status.HTTP_404_NOT_FOUND)


    token,created = Token.objects.get_or_create(user=user)
    serializer = userserializer(instance=user)

    return Response({"token":token.key, "user": serializer.data})






