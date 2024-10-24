import json
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.http import JsonResponse 
from django.conf import settings
# from .models import User,user_otp
from django.utils import timezone
from app.models.clinic_models import Clinic_Registration,Branch_Create
from app.models.email_models import user_otp

from app.models.patient_models import Patient,Patient_Appointment,Patient_Registration
from app.models.Staff_models import Staff_Allotment,Staff_MetaData

import random
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from rest_framework.decorators import api_view




@csrf_exempt
@api_view(['POST'])
def clinic_reg(request):
    try:
        # Check if a clinic already exists
        if Clinic_Registration.objects.exists():
            return JsonResponse({
                "message": "A clinic is already registered. You cannot create another clinic.","status": 400}, status=400)
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        clinic_mobile_number = data.get('clinic_mobile_number')
        address = data.get('address')
        mobile_number = data.get('mobile_number')
        clinic_name = data.get('clinic_name')
        
        # Check if username already exists
        if Clinic_Registration.objects.filter(clinic_username=username).exists():
            return JsonResponse({
                "message": "Username already exists","status": 400}, status=400)
        
        # Create Clinic Registration
        clinic_reg = Clinic_Registration.objects.create(
            clinic_name=clinic_name,
            clinic_mobile_number=clinic_mobile_number,
            clinic_username=username,
            password=password,  
            email=email,
            address=address,
            mobile_number=mobile_number
        )
        create_branch = Branch_Create.objects.create(clinic=clinic_reg)
        return JsonResponse({
            "message": "Clinic Successfully Registered",
            "clinic_id": clinic_reg.clinic_id,
            "status": 201
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            "message": "Invalid JSON format. Please check the request body.","status": 400}, status=400)
    except KeyError as e:
        return JsonResponse({
            "message": f"Missing key in request body: {str(e)}","status": 400}, status=400)
    except TypeError as e:
        return JsonResponse({
            "message": f"Type error: {str(e)}. Please ensure all fields are correctly formatted.","status": 400}, status=400)
    except ValueError as e:
        return JsonResponse({
            "message": f"Value error: {str(e)}. Please check the input values.","status": 400}, status=400)
    except Exception as e:
        return JsonResponse({"message": f"An unexpected error occurred: {str(e)}","status": 500}, status=500)
    

@csrf_exempt
@api_view(['GET'])
def get_clinic_data(request, clinic_id):
    try:
        clinic = Clinic_Registration.objects.get(clinic_id=clinic_id)
        clinic_data = {
            "clinic_id": clinic.clinic_id,
            "clinic_name": clinic.clinic_name,
            "clinic_mobile_number": clinic.clinic_mobile_number,
            "username": clinic.clinic_username,
            "email": clinic.email,
            "mobile_number": clinic.mobile_number,
            "address": clinic.address,
        }
        return JsonResponse(clinic_data)
    except Clinic_Registration.DoesNotExist:
        return JsonResponse({"message": "Clinic does not exist", "status":"400"})
    except Exception as e:
        return JsonResponse({"message": f"An unexpected error occurred: {str(e)}", "status":"500"})    




@csrf_exempt
@api_view(['POST'])
def update_clinic(request):
    try:
        data = json.loads(request.body)
        clinic_id = data.get('clinic_id')

        # Check if the clinic exists
        if Clinic_Registration.objects.filter(clinic_id=clinic_id).exists():
            clinic_obj = Clinic_Registration.objects.get(clinic_id=clinic_id)

            # Update fields if provided in the request data
            clinic_obj.clinic_name = data.get('clinic_name', clinic_obj.clinic_name)
            clinic_obj.email = data.get('email', clinic_obj.email)
            clinic_obj.address = data.get('address', clinic_obj.address)
            clinic_obj.clinic_mobile_number = data.get('clinic_mobile_number', clinic_obj.clinic_mobile_number)
            clinic_obj.clinic_username = data.get('username', clinic_obj.clinic_username)
            clinic_obj.password = data.get('password', clinic_obj.password)  # No hashing here
            clinic_obj.mobile_number = data.get('mobile_number', clinic_obj.mobile_number)

            # Save the updated object
            clinic_obj.save()

            return JsonResponse({"message": "Clinic data updated successfully"}, status=200)
        else:
            return JsonResponse({"message": "Clinic not found"}, status=404)
    
    except Exception as e:
        return JsonResponse({"message": f"An unexpected error occurred: {str(e)}"}, status=500)
  


@csrf_exempt
@api_view(['POST'])
def clinic_login(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if username and password:
            try:
                clinic = Clinic_Registration.objects.get(clinic_username=username)
                
                # Check if the password matches
                if clinic.password == password:  # Direct password comparison
                    return JsonResponse({
                        "message": "Clinic Login successful","clinic_id": clinic.clinic_id,"status": 200}, status=200)
                else:
                    return JsonResponse({
                        "message": "Invalid username or password.","status": 401}, status=401) 
            except Clinic_Registration.DoesNotExist:
                return JsonResponse({
                    "message": "Invalid username or password.","status": 401}, status=401)
        
        return JsonResponse({
            "message": "Username and password are required.","status": 400}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({
            "message": "Invalid JSON format. Please check the request body.","status": 400}, status=400)
    except Exception as e:
        return JsonResponse({
            "message": f"An unexpected error occurred: {str(e)}","status": 500}, status=500)


from django.db import connection

def reset_auto_increment():
    with connection.cursor() as cursor:
        # Replace `clinic_registration` with the correct table name if needed
        cursor.execute("ALTER TABLE app_clinic_registration AUTO_INCREMENT = 1;")



@csrf_exempt
@api_view(['POST'])
def create_branch(request):
    try:
        data = json.loads(request.body)
        clinic_id = data.get('clinic_id')
        branch_name = data.get('branch_name')
        email = data.get('email')
        address = data.get('address')
        password = data.get('password')
        mobile_number = data.get('mobile_number')  # Remove the comma

        # Check if the clinic exists
        try:
            clinic = Clinic_Registration.objects.get(clinic_id=clinic_id)
        except Clinic_Registration.DoesNotExist:
            return JsonResponse({"message": "Clinic does not exist", "status": 400}, status=400)
        
        # Check if a branch with the same name already exists for this clinic
        if Branch_Create.objects.filter(clinic=clinic, branch_name=branch_name).exists():
            return JsonResponse({"message": "A branch with this name already exists for the specified clinic", "status": 400}, status=400)
        
        # Create Branch
        branch_create = Branch_Create.objects.create(
            clinic=clinic,
            branch_name=branch_name,
            email=email,
            address=address,
            mobile_number=mobile_number,
            password=password
        )
        
        return JsonResponse({"message": "Branch successfully created", "branch_id": branch_create.branch_id, "status": 201}, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON format. Please check the request body.", "status": 400}, status=400)
    except KeyError as e:
        return JsonResponse({"message": f"Missing key in request body: {str(e)}", "status": 400}, status=400)
    except TypeError as e:
        return JsonResponse({"message": f"Type error: {str(e)}. Please ensure all fields are correctly formatted.", "status": 400}, status=400)
    except ValueError as e:
        return JsonResponse({"message": f"Value error: {str(e)}. Please check the input values.", "status": 400}, status=400)
    except Exception as e:
        return JsonResponse({"message": f"An unexpected error occurred: {str(e)}", "status": 500}, status=500)




@csrf_exempt
@api_view(['POST'])
def update_branch(request):
    try:
        data = json.loads(request.body)
        branch_id = data.get('branch_id')
        clinic_id = data.get('clinic_id')
        branch_name = data.get('branch_name')
        email = data.get('email')
        address = data.get('address')
        mobile_number = data.get('mobile_number')
        
        # Check if the branch exists
        try:
            branch = Branch_Create.objects.get(branch_id=branch_id)
        except Branch_Create.DoesNotExist:
            return JsonResponse({"message": "Branch does not exist", "status": 400}, status=400)
        
        # Check if the clinic exists
        try:
            clinic = Clinic_Registration.objects.get(clinic_id=clinic_id)
        except Clinic_Registration.DoesNotExist:
            return JsonResponse({"message": "Clinic does not exist", "status": 400}, status=400)
        
        # Update Branch details
        branch.clinic = clinic
        branch.branch_name = branch_name
        branch.email = email
        branch.address = address
        branch.mobile_number = mobile_number
        branch.save()
        
        return JsonResponse({"message": "Branch successfully updated", "status": 200}, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON format. Please check the request body.", "status": 400}, status=400)
    except KeyError as e:
        return JsonResponse({"message": f"Missing key in request body: {str(e)}", "status": 400}, status=400)
    except TypeError as e:
        return JsonResponse({"message": f"Type error: {str(e)}. Please ensure all fields are correctly formatted.", "status": 400}, status=400)
    except ValueError as e:
        return JsonResponse({"message": f"Value error: {str(e)}. Please check the input values.", "status": 400}, status=400)
    except Exception as e:
        return JsonResponse({"message": f"An unexpected error occurred: {str(e)}", "status": 500}, status=500)


@csrf_exempt
@api_view(['GET'])
def get_branch_data(request, branch_id):
    try:
        branch = Branch_Create.objects.get(branch_id=branch_id)
        branch_data = {
            "branch_id": branch.branch_id,
            "clinic_id": branch.clinic.clinic_id,
            "branch_name": branch.branch_name,
            "email": branch.email,
            "mobile_number": branch.mobile_number,
            "address": branch.address,
        }
        return JsonResponse(branch_data)
    except Branch_Create.DoesNotExist:
        return JsonResponse({"message": "Branch does not exist", "status":"404"})
    except Exception as e:
        return JsonResponse({"message": f"An unexpected error occurred: {str(e)}", "status":"500"})
    

@csrf_exempt
@api_view(['GET'])
def get_all_branches(request):
    try:
        # Get clinic_id from query parameters
        clinic_id = request.GET.get('clinic_id')
        
        # Check if the clinic exists
        try:
            clinic = Clinic_Registration.objects.get(clinic_id=clinic_id)
        except Clinic_Registration.DoesNotExist:
            return JsonResponse({"message": "Clinic does not exist", "status": 400}, status=400)
        
        # Get all branches associated with the clinic
        branches = Branch_Create.objects.filter(clinic=clinic)
        
        # Create a list of branch details
        branch_list = [{
            "branch_id": branch.branch_id,
            "branch_name": branch.branch_name,
            "email": branch.email,
            "address": branch.address,
            "mobile_number": branch.mobile_number
        } for branch in branches]
        
        return JsonResponse({
            "clinic_id": clinic.clinic_id,
            "clinic_name": clinic.clinic_name,
            "branches": branch_list,
            "status": 200
        }, status=200)
        
    except Exception as e:
        return JsonResponse({"message": f"An unexpected error occurred: {str(e)}", "status": 500}, status=500)

    
@csrf_exempt
@api_view(['POST'])
def branch_login(request):
    try:
        print(f"Request body: {request.body.decode('utf-8')}")  
        data = json.loads(request.body)
        print(f"Parsed JSON data: {data}") 

        branch_name = data.get('branch_name')
        password = data.get('password')

        print(f"Received branch_name: {branch_name}")
        print(f"Received password: {password}")

        if branch_name is None or password is None:
            return JsonResponse({"message": "branch_name and password are required", "status": 400}, status=400)

        # Check if branch exists with the provided credentials
        try:
            branch = Branch_Create.objects.get(branch_name=branch_name, password=password)
            print(f"Found branch: {branch}")
        except Branch_Create.DoesNotExist:
            return JsonResponse({"message": "Invalid branch name or password", "status": 400}, status=400)

        # If successful, return branch details
        return JsonResponse({
            "message": "Login successful",
            "branch_id": branch.branch_id,
            "branch_name": branch.branch_name,
            "clinic_id": branch.clinic.clinic_id,
            "email": branch.email,
            "address": branch.address,
            "mobile_number": branch.mobile_number,
            "status": 200
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON format. Please check the request body.", "status": 400}, status=400)
    except KeyError as e:
        return JsonResponse({"message": f"Missing key in request body: {str(e)}", "status": 400}, status=400)
    except Exception as e:
        return JsonResponse({"message": f"An unexpected error occurred: {str(e)}", "status": 500}, status=500)


@csrf_exempt
def send_signin_otp(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            email = data.get('email')
            
            if email:
                otp = random.randint(1000, 9999)
                request.session['otp'] = otp
                request.session['otp_timestamp'] = time.time()  # Store the time when OTP was generated
                
                send_mail(
                    'Your SignIn OTP Code',  #subject
                    f'Your SignIn OTP code is {otp}',  #message
                    settings.DEFAULT_FROM_EMAIL,  #default sender email from settings.py
                    [email],
                    fail_silently=False,
                )
                return JsonResponse({'message': 'SignIn OTP sent', 'status': 200}, status=200)
            else:
                return JsonResponse({'error': 'Email is required', 'status': 400}, status=400)
        
        return JsonResponse({'error': 'Invalid request method', 'status': 405}, status=405)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format', 'status': 400}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e), 'status': 500}, status=500)
    
 