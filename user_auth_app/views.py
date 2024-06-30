from datetime import datetime, time, timedelta
import re
from googleapiclient.discovery import build
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from .models import UserProfile
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.hashers import make_password, check_password
import os
from django.conf import settings

BASE_DIR = settings.BASE_DIR



def index(request):
    return render(request, 'user_auth_app/index.html')


def signup(request):
    if request.method == 'POST':
        try:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            profilepic = request.FILES['profilepicture']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirmpassword']
            address_line1 = request.POST['addressline1']
            city = request.POST['city']
            state = request.POST['state']
            pincode = request.POST['pincode']
            user_type = request.POST['usertype']
            if user_type == 'doctor':
                specialization = request.POST['specialization']
            else:
                specialization = ''

            if UserProfile.objects.filter(username=username).exists():
                return render(request, 'user_auth_app/signup.html', {'error': "Username already exists. Please choose a different one."})

            if password == confirm_password:
                hashed_password = make_password(password)
                user = UserProfile(first_name=firstname, last_name=lastname, profile_picture=profilepic, username=username,
                                   email=email, password=hashed_password, address_line1=address_line1, city=city, state=state,
                                   pincode=pincode, user_type=user_type, specialization=specialization)
                user.save()
                return redirect('/login/')

        except MultiValueDictKeyError as e:
            print(f"KeyError: {e}")
            return render(request, 'user_auth_app/signup.html', {'error': "Some form fields are missing."})
    else:
        return render(request, 'user_auth_app/signup.html')


def login(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            entered_password = request.POST['password']

            try:
                user = UserProfile.objects.get(username=username)
            except UserProfile.DoesNotExist:
                return render(request, 'user_auth_app/login.html', {'error': "Invalid Credentials!"})

            if check_password(entered_password, user.password):
                if user.user_type == 'doctor':
                    redirect_url = f'/doctor-dashboard/?username={username}'
                    return redirect(redirect_url)

                elif user.user_type == 'patient':
                    return redirect(f'/patient-dashboard/?username={username}')

                else:
                    return render(request, 'user_auth_app/login.html', {'error': "Invalid user type."})
            else:
                return render(request, 'user_auth_app/login.html', {'error': "Invalid Credentials!"})

        except MultiValueDictKeyError as e:
            print(f"KeyError: {e}")
            return render(request, 'user_auth_app/login.html', {'error': "Some form fields are missing."})
    else:
        return render(request, 'user_auth_app/login.html')


def patient_dashboard(request):
    try:
        username = request.GET.get('username', None)
        user = UserProfile.objects.get(username=username)
        return render(request, 'user_auth_app/dashboard_patient.html', {'user': user})
    except UserProfile.DoesNotExist:
        return HttpResponse("User not found", status=404)


def doctor_dashboard(request):
    try:
        username = request.GET.get('username', None)
        user = UserProfile.objects.get(username=username)
        return render(request, 'user_auth_app/dashboard_doctor.html', {'user': user})
    except UserProfile.DoesNotExist:
        return HttpResponse("User not found", status=404)
