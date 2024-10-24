# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from django.views.decorators.csrf import csrf_exempt
# import json
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from rest_framework.response import Response
# from django.http import JsonResponse 
# from django.conf import settings
# # from .models import User,user_otp
# from django.utils import timezone
# from app.models.clinic_models import Clinic_Registration,Branch_Create
# from app.models.email_models import user_otp

# from app.models.patient_models import Patient,Patient_Appointment,Patient_Registration
# from app.models.Staff_models import Staff_Allotment,Staff_MetaData



# # from .models import Clinic_Registration,Branch_Create,Staff_Allotment,Staff_MetaData,Patient_Appointment
# from django.core.mail import send_mail

# from .serializers import (
#    StaffSerializer,PatientCreateSerializer
# )








   
# # # Set a minimum interval between OTP resends (e.g., 60 seconds)
# # RESEND_INTERVAL = 60  # Allow resending OTP every 60 seconds

# import random
# from django.core.mail import send_mail
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# import json

# # @csrf_exempt
# # def resend_signin_otp(request):
# #     try:
# #         if request.method == 'POST':
# #             data = json.loads(request.body)
# #             email = data.get('email')

# #             if email:
# #                 # Generate a new OTP and update the session
# #                 otp = random.randint(1000, 9999)
# #                 request.session['otp'] = otp
# #                 request.session['otp_timestamp'] = time.time()  # Store the new OTP timestamp

# #                 # Send OTP via email
# #                 send_mail(
# #                     'Your Resend OTP Code',
# #                     f'Your OTP code is {otp}',
# #                     settings.DEFAULT_FROM_EMAIL,  # Use the default sender email from settings.py
# #                     [email],
# #                     fail_silently=False,
# #                 )
# #                 return JsonResponse({'message': 'OTP resent successfully', 'status': 200}, status=200)
            
# #             return JsonResponse({'error': 'Email is required', 'status': 400}, status=400)

# #         return JsonResponse({'error': 'Invalid request method', 'status': 405}, status=405)

# #     except json.JSONDecodeError:
# #         return JsonResponse({'error': 'Invalid JSON format', 'status': 400}, status=400)
# #     except Exception as e:
# #         return JsonResponse({'error': str(e), 'status': 500}, status=500)


# # @csrf_exempt
# # def user_signIn(request):
# #     if request.method == 'POST':
# #         try:
# #             data = json.loads(request.body)
# #             email = data.get('email')
# #             mobile_number = data.get('mobile_number')
# #             otp = data.get('otp')

# #             if not email and not mobile_number:
# #                 return JsonResponse({'error': 'Email or mobile number is required', 'status': 400}, status=400)

# #             if email:
# #                 user = Staff_Allotment.objects.filter(email=email).first()
# #             elif mobile_number:
# #                 user = Staff_Allotment.objects.filter(mobile_number=mobile_number).first()

# #             if user:
# #                 # Check OTP only for email sign-in
# #                 if email:
# #                     if not otp:
# #                         return JsonResponse({'error': 'OTP is required for email sign-in', 'status': 400}, status=400)
                    
# #                     session_otp = request.session.get('otp')
# #                     otp_timestamp = request.session.get('otp_timestamp')

# #                     if session_otp and otp_timestamp:
# #                         if time.time() - otp_timestamp > OTP_EXPIRY_TIME:
# #                             return JsonResponse({'error': 'OTP has expired', 'status': 400}, status=400)

# #                         if otp != str(session_otp):
# #                             return JsonResponse({'error': 'Invalid OTP', 'status': 400}, status=400)

# #                         # OTP is valid, proceed with login
# #                         del request.session['otp']
# #                         del request.session['otp_timestamp']
# #                         return JsonResponse({"message": "Sign-in successful", "status": 200}, status=200)
# #                     else:
# #                         return JsonResponse({'error': 'OTP not found or expired', 'status': 400}, status=400)
                
# #                 # For mobile sign-in, no OTP is required
# #                 return JsonResponse({"message": "Sign-in successful", "status": 200}, status=200)
# #             else:
# #                 return JsonResponse({"error": "User not found", "status": 404}, status=404)

# #         except json.JSONDecodeError:
# #             return JsonResponse({'error': 'Invalid JSON format', 'status': 400}, status=400)
# #         except Exception as e:
# #             return JsonResponse({'error': str(e), 'status': 500}, status=500)

# #     return JsonResponse({'error': 'Invalid request method', 'status': 405}, status=405)


# # Define OTP expiry time (e.g., 5 minutes)
# OTP_EXPIRY_TIME = 300  # 300 seconds = 5 minutes


# from django.core.mail import send_mail
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# import json
# import random
# import time

# # @csrf_exempt
# # def send_registration_otp(request):
# #     try:
# #         if request.method == 'POST':
# #             data = json.loads(request.body)
# #             email = data.get('email')
            
# #             if email:
# #                 otp = random.randint(1000, 9999)
# #                 request.session['otp'] = otp
# #                 request.session['otp_timestamp'] = time.time()  # Store the time when OTP was generated
                
# #                 # Send registration OTP email
# #                 send_mail(
# #                     'Your Registration OTP Code',  # Updated subject for registration
# #                     f'Your Registration OTP code is {otp}',  # Updated message for registration
# #                     settings.DEFAULT_FROM_EMAIL,  # Use the default sender email from settings.py
# #                     [email],
# #                     fail_silently=False,
# #                 )
# #                 return JsonResponse({'message': 'Registration OTP sent', 'status': 200}, status=200)
# #             else:
# #                 return JsonResponse({'error': 'Email is required', 'status': 400}, status=400)
        
# #         return JsonResponse({'error': 'Invalid request method', 'status': 405}, status=405)
    
# #     except json.JSONDecodeError:
# #         return JsonResponse({'error': 'Invalid JSON format', 'status': 400}, status=400)
# #     except Exception as e:
# #         return JsonResponse({'error': str(e), 'status': 500}, status=500)



# # @csrf_exempt
# # def resend_registration_otp(request):
# #     try:
# #         if request.method == 'POST':
# #             data = json.loads(request.body)
# #             email = data.get('email')

# #             if email:
# #                 # Generate a new OTP and update the session
# #                 otp = random.randint(1000, 9999)
# #                 request.session['otp'] = otp
# #                 request.session['otp_timestamp'] = time.time()  # Store the new OTP timestamp

# #                 # Send registration OTP via email
# #                 send_mail(
# #                     'Your Resend Registration OTP Code',  # Updated subject for resend
# #                     f'Your Registration OTP code is {otp}',  # Updated message for resend
# #                     settings.DEFAULT_FROM_EMAIL,  # Use the default sender email from settings.py
# #                     [email],
# #                     fail_silently=False,
# #                 )
# #                 return JsonResponse({'message': 'Registration OTP resent successfully', 'status': 200}, status=200)
            
# #             return JsonResponse({'error': 'Email is required', 'status': 400}, status=400)

# #         return JsonResponse({'error': 'Invalid request method', 'status': 405}, status=405)

# #     except json.JSONDecodeError:
# #         return JsonResponse({'error': 'Invalid JSON format', 'status': 400}, status=400)
# #     except Exception as e:
# #         return JsonResponse({'error': str(e), 'status': 500}, status=500)













# # @api_view(['POST'])
# # def registerPatientNow(request):
# #     if request.method == 'POST':
# #         patient_data = {
# #             'patient_name': request.data.get('patient_name'),
# #             'mobile_number': request.data.get('mobile_number'),
# #             'email': request.data.get('email'),
# #             'gender': request.data.get('gender'),
# #             'address': request.data.get('address'),
# #             'date_of_birth': request.data.get('date_of_birth'),
# #             'is_registered': True
# #         }

# #         patient_serializer = PatientCreateSerializer(data=patient_data)
# #         if patient_serializer.is_valid():
# #             patient = patient_serializer.save()
# #             return Response({
# #                 "message": "Patient registered successfully",
# #                 "patient": {
# #                     "patient_id": patient.patient_id,
# #                     "patient_name": patient.patient_name,
# #                     "mobile_number": patient.mobile_number,
# #                     "email": patient.email,
# #                     "gender": patient.gender,
# #                     "address": patient.address,
# #                     "date_of_birth": patient.date_of_birth,
# #                     "age": patient_serializer.data['age']
# #                 }
# #             }, status=status.HTTP_201_CREATED)
# #         return Response({
# #             "error": "Failed to register patient",
# #             "details": patient_serializer.errors
# #         }, status=status.HTTP_400_BAD_REQUEST)


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import PatientCreateSerializer
# from django.db import transaction




# # from rest_framework.decorators import api_view
# # from rest_framework.response import Response
# # from rest_framework import status
# # from .models import Patient_Registration
# # from .serializers import PatientCreateSerializer
# # from datetime import datetime

# # @api_view(['POST'])
# # def registerPatientNow(request):
# #     if request.method == 'POST':
# #         # Extract patient data from the request
# #         patient_data = {
# #             'patient_name': request.data.get('patient_name'),
# #             'mobile_number': request.data.get('mobile_number'),
# #             'email': request.data.get('email'),
# #             'gender': request.data.get('gender'),
# #             'address': request.data.get('address'),
# #             'date_of_birth': request.data.get('date_of_birth'),
# #             'is_registered': True
# #         }

# #         # Serialize the patient data
# #         patient_serializer = PatientCreateSerializer(data=patient_data)
# #         if patient_serializer.is_valid():
# #             # Save the patient record to the database
# #             patient = patient_serializer.save()

# #             # Generate the next patient_id
# #             last_patient = Patient_Registration.objects.order_by('-patient_id').first()
# #             if last_patient and last_patient.patient_id:
# #                 try:
# #                     last_code_int = int(last_patient.patient_id[3:])
# #                 except ValueError:
# #                     last_code_int = 0  # Default to 0 if conversion fails
# #                 next_code_int = last_code_int + 1
# #             else:
# #                 next_code_int = 1
            
# #             patient_id = f"SER{next_code_int:03d}"
            
# #             # Update the patient record with the new patient_id
# #             patient.patient_id = patient_id
# #             patient.save()

# #             return Response({
# #                 "message": "Patient registered successfully",
# #                 "patient": {
# #                     "patient_id": patient.patient_id,
# #                     "patient_name": patient.patient_name,
# #                     "mobile_number": patient.mobile_number,
# #                     "email": patient.email,
# #                     "gender": patient.gender,
# #                     "address": patient.address,
# #                     "date_of_birth": patient.date_of_birth,
# #                     "age": calculate_age(patient.date_of_birth)  # Ensure age is calculated correctly
# #                 }
# #             }, status=status.HTTP_201_CREATED)
        
# #         return Response({
# #             "error": "Failed to register patient",
# #             "details": patient_serializer.errors
# #         }, status=status.HTTP_400_BAD_REQUEST)

# # def calculate_age(date_of_birth):
# #     today = datetime.today()
# #     birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')
# #     age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
# #     return age


 


# # from django.http import JsonResponse
# # from .models import Patient_Registration, Patient_Appointment, Staff_Allotment, Staff_MetaData
# # from rest_framework.decorators import api_view
# # from django.views.decorators.csrf import csrf_exempt
# # import json

# # @api_view(['POST'])
# # @csrf_exempt
# # def schedule_appointment(request):
# #     if request.method == 'POST':
# #         try:
# #             data = json.loads(request.body)
# #             is_registered = data.get('is_registered', False)
# #             doctor_id = data.get('doctor')
# #             appointment_type = data.get('appointment_type')
# #             appointment_date = data.get('appointment_date')
# #             from_time = data.get('from_time')
# #             to_time = data.get('to_time')
# #             notes = data.get('notes')

# #             if is_registered:
# #                 # Handle registered patient
# #                 patient_id = data.get('patient_id')
# #                 try:
# #                     patient = Patient_Registration.objects.get(patient_id=patient_id)
# #                 except Patient_Registration.DoesNotExist:
# #                     return JsonResponse({'error': 'Patient ID not found', 'status': 404}, status=404)
# #             else:
# #                 # Handle non-registered patient
# #                 patient_name = data.get('patient_name')
# #                 mobile_number = data.get('mobile_number')
# #                 email = data.get('email')

# #                 if not patient_name:
# #                     return JsonResponse({'error': 'Patient name is required for non-registered patients', 'status': 400}, status=400)

# #                 if not mobile_number:
# #                     return JsonResponse({'error': 'Mobile number is required for non-registered patients', 'status': 400}, status=400)
                
# #                 # Check if mobile number is already used
# #                 if Patient_Registration.objects.filter(mobile_number=mobile_number).exists():
# #                     return JsonResponse({'error': 'Mobile number already in use', 'status': 400}, status=400)
                
# #                 # Create a new non-registered patient
# #                 patient = Patient_Registration.objects.create(
# #                     patient_name=patient_name,
# #                     mobile_number=mobile_number,
# #                     email=email,
# #                     is_registered=False  # Non-registered patients
# #                 )

# #             # Fetch doctor details
# #             try:
# #                 doctor = Staff_Allotment.objects.get(staff_id=doctor_id)
# #                 doctor_metadata = Staff_MetaData.objects.get(staff_id=doctor_id)
# #             except Staff_Allotment.DoesNotExist:
# #                 return JsonResponse({'error': 'Doctor not found', 'status': 404}, status=404)
# #             except Staff_MetaData.DoesNotExist:
# #                 return JsonResponse({'error': 'Doctor metadata not found', 'status': 404}, status=404)

# #             # Create the appointment
# #             appointment = Patient_Appointment.objects.create(
# #                 patient=patient.patient_id if is_registered else None,
# #                 patient_name=patient.patient_name if not is_registered else None,
# #                 mobile_number=mobile_number if not is_registered else None,
# #                 email=email if not is_registered else None,
# #                 doctor=doctor,
# #                 appointment_type=appointment_type,
# #                 appointment_date=appointment_date,
# #                 from_time=from_time,
# #                 to_time=to_time,
# #                 notes=notes,
# #                 is_registered=is_registered
# #             )

# #             # Prepare the response data
# #             response_data = {
# #                 'appointment_id': appointment.appointment_id,
# #                 'appointment_type': appointment.appointment_type,
# #                 'appointment_date': appointment.appointment_date,
# #                 'from_time': appointment.from_time,
# #                 'to_time': appointment.to_time,
# #                 'notes': appointment.notes,
# #                 'patient_id': patient.patient_id if is_registered else None,
# #                 'patient_name': patient.patient_name if not is_registered else None,
# #                 # 'patient_name': patient.patient_name if patient.patient_name else patient_name,

# #                 'patient_name': patient.patient_name if is_registered else None,
# #                 'doctor': doctor.staff_id,
# #                 'doctor_name': doctor.username,
# #                 'speciality': doctor_metadata.speciality,
# #                 'is_registered': is_registered
# #             }

# #             return JsonResponse({
# #                 'message': 'Appointment booked successfully',
# #                 'data': response_data
# #             }, status=200)

# #         except json.JSONDecodeError:
# #             return JsonResponse({'error': 'Invalid JSON format', 'status': 400}, status=400)
# #         except Exception as e:
# #             return JsonResponse({'error': str(e), 'status': 500}, status=500)

# #     return JsonResponse({'error': 'Invalid request method', 'status': 405}, status=405)

