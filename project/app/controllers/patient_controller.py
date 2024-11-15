import time
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.http import JsonResponse 
from django.conf import settings
from app.models.patient_models import Patient
from app.models.email_models import user_otp
# from app.models import User,user_otp

from app.models.patient_models import Patient,Patient_Appointment,Patient_Registration
from django.utils import timezone
from app.serializers import*
import jwt

from django.http import Http404
from app.controllers.email_controller import create_notification
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
# from django.http.HttpRequest 
from decimal import Decimal

class CouponsAPIView(APIView):

    def get(self, request, coupon_id=None):
        if coupon_id:
            coupon = get_object_or_404(Coupons, coupon_id=coupon_id)
            serializer = CouponsSerializer(coupon)
            return JsonResponse({"status": "200", "data": serializer.data})
        else:
            coupons = Coupons.objects.all()
            serializer = CouponsSerializer(coupons, many=True)
            return JsonResponse({"status": "200", "data": serializer.data})

    def post(self, request):
        serializer = CouponsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "200", "data": serializer.data})
        return JsonResponse({"status": "400", "errors": serializer.errors})

    def delete(self, request, coupon_id):
        coupon = get_object_or_404(Coupons, coupon_id=coupon_id)
        coupon.delete()
        return JsonResponse({"status": "204", "message": "Coupon deleted successfully"})

    def put(self, request, coupon_id):
        coupon = get_object_or_404(Coupons, coupon_id=coupon_id)
        serializer = CouponsSerializer(coupon, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "200", "data": serializer.data})
        return JsonResponse({"status": "400", "errors": serializer.errors})


class VerifyCoupon(APIView):
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            print("data :",data)

            # Extract data from the request
            coupon_code = request.data.get('coupon_code')
            amount = Decimal(data.get('amount', '0.0'))
            
            if not all([coupon_code,amount]):
                return JsonResponse({'error': 'Missing required parameters.',"status":"404"}, status="404")
            
            # Check if the coupon exists
            try:
                coupon = Coupons.objects.get(coupon_code=coupon_code)
            except Coupons.DoesNotExist:
                return JsonResponse({'error': 'Invalid coupon code.',"status":"405"}, status=405)
            
            
            coupon_obj = Coupons.objects.get(coupon_code=coupon,is_active=True)
            current_date = timezone.now().date()            
            
            if not (coupon_obj.valid_from <= current_date <= coupon_obj.valid_till):
                    return JsonResponse({'error': 'Coupon is not valid on the current date.', "status": "401"}, status=401)
            else  :
                coupon_obj = Coupons.objects.get(coupon_code=coupon,is_active=True)
                
                coupon_percentage = coupon_obj.percentage
                amount_claimed=(amount * coupon_percentage / 100)
                amount = amount - (amount * coupon_percentage / 100)
            
                return JsonResponse({"message" :"Coupon is verified","amount":amount ,"coupon_applied":True,"amount_deducted":amount_claimed,"status":"200" },status=200)

        
        except Exception as e:
            return JsonResponse({'error': str(e),"status":"500"}, status=500)







@api_view(['GET', 'POST'])
def symptom_list(request):
    # GET: List all symptoms or POST: Create a new symptom
    if request.method == 'GET':
        symptoms = Patient_Symptoms.objects.all()
        serializer = PatientSymptomsSerializer(symptoms, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PatientSymptomsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def symptom_detail(request, pk):
    # Retrieve, update, or delete a specific symptom by its primary key (symptom_id)
    try:
        symptom = Patient_Symptoms.objects.get(pk=pk)
    except Patient_Symptoms.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientSymptomsSerializer(symptom)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PatientSymptomsSerializer(symptom, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        symptom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookAppointmentList(APIView):

    parser_classes = [MultiPartParser, FormParser]  # To handle file uploads

    def post(self, request):

        patient = request.user
        serializer = BookAppointmentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            data=serializer.data
            paid_amount=data["net_payable"]
            print(data["net_payable"])
            create_notification(patient.patient_id,
                                            "Quiz_Unsubcription",
                                            f"INR {paid_amount} ")
            # return Response(serializer.data, "status": "400",status=status.HTTP_201_CREATED)

            return Response({"appointment_data": [serializer.data],"status":"200"}, status=200)
        
        else:
            return JsonResponse({'errors': serializer.errors, "status": "400"}, status=400)




class BookAppointmentDetail(APIView):
    def get_object(self, pk):
        try:
            return Book_Appointment.objects.get(pk=pk)
        except Book_Appointment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        appointment = self.get_object(pk)
        serializer = BookAppointmentSerializer(appointment)
        return Response(serializer.data)

    def put(self, request, pk):
        appointment = self.get_object(pk)
        
        # Extract the fields you want to update
        slot_id = request.data.get('slot_id', None)
        appointment_date = request.data.get('appointment_date', None)

        if slot_id and appointment_date:
            # Fetch the slot by ID and check its availability
            try:
                slot = Slot.objects.get(slot_id=slot_id)
                
                if not slot.is_available:
                    return Response({'error': 'This slot is not available.'}, status=status.HTTP_400_BAD_REQUEST)
            except Slot.DoesNotExist:
                return Response({'error': 'Slot does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            # Track the previous slot to mark it as available later
            previous_slot = appointment.slot_id  # Store the previous slot instance

            print("previous_slot :",previous_slot.slot_id)
            # Update the appointment with the new slot and date
            appointment.slot_id = slot  # Assign the Slot instance, not the ID
            appointment.appointment_date = appointment_date
            appointment.save()

            # Mark the new slot as unavailable
            slot.is_available = False
            slot.save()

            # Mark the previous slot as available if it exists
            if previous_slot:
                previous_slot.is_available = True
                previous_slot.save()

            # Serialize and return the updated appointment
            serializer = BookAppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'error': 'slot_id and appointment_date are required.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        appointment = self.get_object(pk)
        appointment.slot_id

        previous_slot = appointment.slot_id  # Store the previous slot instance
        if previous_slot:
                previous_slot.is_available = True
                previous_slot.save()

        appointment.delete()


        return Response(status=status.HTTP_204_NO_CONTENT)
    



# def book_appointment(request):
#     try:
#         data = json.loads(request.POST.get('data', '{}'))
#         print(data)
        
#         is_self = data.get('is_self',True)

#         patient_id = data.get('patient_id')
#         patient_name = data.get('patient_name')
#         age = data.get('age')
#         gender = data.get('gender')
#         relation=data.get('relation')
#         description = data.get('description')
#         symptoms = data.get('symptoms')
#         spotted_place = data.get('spotted_place')
#         patient_id = data.get('patient_id')







        # image1,im = None
        # if request.FILES.get('image'):
        #     image = request.FILES['image']

        # Extract JSON data from form-data

    # except Exception as error:
    #     pass


@api_view(['POST'])
def update_profile_page(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed', "status": "405"}, status=405)

    try:
        # Extract image file if present in request
        image = request.FILES.get('image', None)

        # Extract JSON data from form-data
        data = request.POST.get('data', '{}')
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format', "status": "400"}, status=400)

        # Check if user ID is provided
        user_id = data.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'User ID is required', "status": "400"}, status=400)

        # Check if user exists
        try:
            user = Patient.objects.get(id=user_id)
        except Patient.DoesNotExist:
            return JsonResponse({"message": "User not found", "status": 400}, status=400)

        # Track changes
        changed_fields = []

        # Update user profile if user exists
        serializer = PatientUpdateSerializer(user, data=data, partial=True)
        
        # Handle image outside serializer if present
        if image:
            user.image = image
            changed_fields.append('Profile picture changed')

        if serializer.is_valid():
            # Save other changes
            serializer.save()

            # Track which fields were updated
            for field, value in data.items():
                if hasattr(user, field) and getattr(user, field) != value:
                    changed_fields.append(f"{field} changed to {value}")

            # Create a notification with the changes
            if changed_fields:
                message = "The following fields were updated: " + ", ".join(changed_fields)
                create_notification(user_id, "User Profile Update", message)

            return JsonResponse({'message': 'User updated successfully', "changed_fields": changed_fields, 'status': '200'}, status=200)

        else:
            return JsonResponse({'errors': serializer.errors, "status": "400"}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e), "status": "500"}, status=500)





# @api_view(['POST'])

# def update_profile_page(request):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Only POST requests are allowed',"status": "405"}, status=405)

#     try:
#         # Extract image file if present in request
#         image = request.FILES.get('image', None)

#         # Extract JSON data from form-data
#         data = request.POST.get('data', '{}')
#         try:
#             data = json.loads(data)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON format',"status": "400"}, status=400)

#         # Check if user ID is provided
#         user_id = data.get('user_id')
#         if not user_id:
#             return JsonResponse({'error': 'User ID is required',"status": "400"}, status=400)

#         # Check if user exists
#         try:
#             user = Patient.objects.get(id=user_id)
#         except Patient.DoesNotExist:
#             return JsonResponse({"message": "User not found", "status": 400}, status=400)

#         # Track changes
#         changed_fields = []

#         # Update user profile if user exists
#         serializer = PatientUpdateSerializer(user, data=data, partial=True)
#         if serializer.is_valid():
#             # Save image if provided
#             if image:
#                 user.image = image
#                 changed_fields.append('Profile picture is changed')
#             # Save other changes
#             for field, value in data.items():
#                 if hasattr(user, field) and getattr(user, field) != value:
#                     changed_fields.append(f"{field} changed to {value}")

#             serializer.save()

#             # Create a notification with the changes
#             if changed_fields:
#                 message = "The following fields were updated: " + ", ".join(changed_fields)
#                 create_notification(user_id, "User Profile Update", message)

#             return JsonResponse({'message': 'User updated successfully', "changed_fields": changed_fields, 'status': '200'}, status=200)
        
#         else:
#             return JsonResponse({'errors': serializer.errors,"status": "400"}, status=400)
#     except Exception as e:
#         return JsonResponse({'error': str(e),"status": "500"}, status=500)

# def update_profile_page(request):
#     try:
#         # Extract image file if present in request
#         image = None
#         if request.FILES.get('image'):
#             image = request.FILES['image']

#         # Extract JSON data from form-data
#         data = json.loads(request.POST.get('data', '{}'))
#         print(data)

#         # Check if user ID is provided
#         user_id = data.get('user_id')
#         if not user_id:
#             return JsonResponse({'error': 'User ID is required'}, status=400)

#         # Check if user exists
#         try:
#             user = Patient.objects.get(id=user_id)
#         except Patient.DoesNotExist:
#             return JsonResponse({"message": "User not found", "status": 400}, status=400)

#         # Track changes
#         changed_fields = []

#         # Update user profile if user exists
#         serializer = PatientUpdateSerializer(user, data=data, partial=True)
#         if serializer.is_valid():
#             # Save image if provided
#             if image:
#                 user.image = image
#                 changed_fields.append('Profile picture is changed')
#             # Save other changes
#             for field, value in data.items():
#                 if hasattr(user, field) and getattr(user, field) != value:
#                     changed_fields.append(f"{field} changed to {value}")

#             serializer.save()

#             # Create a notification with the changes
#             if changed_fields:
#                 message = "The following fields were updated: " + ", ".join(changed_fields)
#                 create_notification(user_id, "User Profile Update", message)

#             return JsonResponse({'message': 'User updated successfully', "changed_fields":changed_fields, 'status': '200'}, status=200)
        
#         else:
#             return JsonResponse({'errors': serializer.errors}, status=400)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

from rest_framework.decorators import api_view, authentication_classes,permission_classes

# @permission_classes([IsAuthenticated])
# @api_view(['GET'])

# def get_profile_page(request):

#     patient = request.user

#     try:
#         user = Patient.objects.get(id=patient.id)
#     except json.JSONDecodeError:
#         return JsonResponse({"error": "Invalid JSON format", "status": "402"})
#     except Patient.DoesNotExist:
#         return JsonResponse({'error': 'User not found'}, status=404)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

#     serializer = PatientUpdateSerializer(user)
#     return JsonResponse({"user_data": [serializer.data]})

@api_view(['GET'])
def get_profile_page(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized access"}, status=401)

    patient = request.user
    print("patient :",patient)

    try:
        user = Patient.objects.get(id=patient.id)
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    serializer = PatientUpdateSerializer(user)
    return Response({"user_data": [serializer.data],"status":"200"}, status=200)
import jwt
@csrf_exempt
def login_user(request):

    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            print("data : ",data)
            
            email = data.get('email')
            otp=data.get("otp")

            through_google=data.get('through_google') 
           
            if   through_google == "True" :  
                # print("inif") 
                patient_exists = Patient.objects.filter(email=email,status=True).exists()

                # print(user_exists)
                if patient_exists :

                    secret='django-insecure-%azpy(5fq-z!(&ug@&*cpu@f@)w%u4xo11k=rl)t=x8av(c^mm'
                    payload={
                        "user_id":patient.id,
                        "iat":int(time.time()),
                        "exp":int(time.time())+86400,
                    }


                    print(jwt.__file__)
                    print("@")
                    encoded_jwt = jwt.encode(payload, secret ,algorithm="HS256")
                    print(encoded_jwt)
                    token = jwt.decode(encoded_jwt, secret , algorithms ="HS256")
                    print(token)


                    patient_obj =Patient.objects.get(email=email)
                    return JsonResponse({'message': 'Login successfull',
                                        'user_mail': patient_obj.email,
                                        # "is_creatot":patient_obj.is_creator ,
                                        'username':patient_obj.username,
                                        'user_id':patient_obj.id,
                                        "company_id":1,
                                        "branch_id":1,
                                        "status":"200",
                                        "through_google":True,
                                        "token":token,

                                        }, status=200)                                                           
                    
                else:
                    patient = Patient(email=email,registeredat=timezone.now())
                    patient.save()

                    secret='django-insecure-%azpy(5fq-z!(&ug@&*cpu@f@)w%u4xo11k=rl)t=x8av(c^mm'
                    payload={
                        "user_id":patient.id,
                        "iat":int(time.time()),
                        "exp":int(time.time())+(30*86400),
                    }


                    encoded_jwt = jwt.encode(payload, secret ,algorithm="HS256")
                    # print(encoded_jwt)
                    token = jwt.decode(encoded_jwt, secret , algorithms ="HS256")
                    # print(token)



                    return JsonResponse({'message': 'Login successfull',
                                        'user_mail': patient.email,
                                        'username':patient.username,
                                        "name":patient.name,
                                        # "is_creatot":patient.is_creator,
                                        'user_id':patient.id,
                                        "company_id":1,
                                        "branch_id":1,
                                        "status":"200",
                                        "through_google":False,
                                        "token":token,
                                        }, status=200)         
            else:
                
                exists = Patient.objects.filter(email=email,is_active=True).exists()
                if exists:
                        try:
                            if email != '' and otp != '' :
                                    print(otp)
                                    
                                    
                                    stored_otp=user_otp.objects.get(user_email=email,purpose="login")
                                    print("stored_otp :",stored_otp,otp)
                                    stored_otp=stored_otp.otp
                                    print("stored_otp :",stored_otp,otp)
                                    print(otp == stored_otp)
                                    if(otp == stored_otp) :
                                        patient= Patient.objects.get(email=email)
                                        print("user",patient)


                                        # secret='django-insecure-%azpy(5fq-z!(&ug@&*cpu@f@)w%u4xo11k=rl)t=x8av(c^mm'

                                        secret=settings.SECRET_KEY
                                        payload={
                                                "patient_id":patient.id,
                                                "iat":int(time.time()),
                                                "exp":int(time.time())+86400,
                                                }
                                        encoded_jwt = jwt.encode(payload, secret ,algorithm="HS256")
                                        print(encoded_jwt)
                                        token = jwt.decode(encoded_jwt, secret , algorithms ="HS256")
                                        print(token)
                                        user_otp.objects.filter(user_email=email).delete()

                                        

                                        return JsonResponse({'message': 'Login successful',
                                                             
                                                             
                                            'user email': patient.email,
                                            # "is_creator":patient.is_creator,                                            
                                            'username':patient.username,
                                            "name":patient.name,
                                            'user id':patient.id,
                                            "company_id":1,
                                            "branch id":1,
                                            "status":"200",
                                            "through_google":patient.through_google,
                                            'token':encoded_jwt}, status=200)
                                        

                                    else:
                                        return JsonResponse({'message': 'Entered Wrong OTP', 'status': '402'}, status=402)
                                    
                                  
                            else:
                                return JsonResponse({'message': 'Enter valid Details', 'status': '403'}, status=403)         
                        except Exception as e:
                                return JsonResponse({'message': str(e), 'status': '403'}, status=403) 
                else:
                    return JsonResponse({'error': 'User does not exist', "status":"404"}, status=404)
        
        else:
            return JsonResponse({'error': 'Only POST requests are allowed', "status":"405"}, status=405)
    except Exception as error :
            return JsonResponse({'message': 'Server Error', "status":"500","error":error}, status=500) 

from django.utils import timezone

from app.models.wallet_models import wallet

@csrf_exempt
def register_user(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            print(data)
            
            email = data.get('email')
            username = data.get('username')
            otp =data.get('otp')
            mobile=data.get('mobile')
            # fcm_token=data.get('fcm_token','null')

            try:
                if email != '' and username != '' and otp != '' and mobile != '':
                    # user=User.objects.get(email=email)
                    exists = Patient.objects.filter(email=email).exists()
                    print("exist :",exists)
                    if exists:
                        return JsonResponse({'message': 'Email already registered', 'status': '401'}, status=401)
                
                    if Patient.objects.filter(username=username).exists():
                        return JsonResponse({'message': 'Username already exists', 'status': '409'}, status=409)
                
                    else:
                        stored_obj=user_otp.objects.get(user_email=email,purpose="signup")
                        # print("stored_otp :",stored_obj,otp)
                        stored_otp=stored_obj.otp
                        print("stored_otp :",stored_otp,otp)
                        print(otp == stored_otp)
                        
                        if(otp == stored_otp):
                            print("1")              
                            # user = Patient.objects.create(email=email,registeredat=timezone.now(),username=username,mobile=mobile,fcm_token=fcm_token)
                            # user.save()
                            print("2")              

                            print("3")              

                            # user=user

                            patient = Patient.objects.create(email=email,registeredat=timezone.now(),username=username,mobile=mobile)
                            patient_id=patient
                            print("patient id",patient_id)
                            wallets=wallet.objects.create(patient_id=patient_id,wallet_bal=1000,email=patient_id)
                            print("wallet :",wallets)
                            # wallets.save()
                            stored_obj.delete()
                            print("4")      



                            return JsonResponse({'message': 'User registered successfully', 'status': '200'}, status=200)
                        else:
                            return JsonResponse({'message': 'Entered Wrong OTP', 'status': '402'}, status=402)
                else:
                    return JsonResponse({'message': 'Enter valid Details', 'status': '403'}, status=403)         
            except Exception as e:
                return JsonResponse({'message': str(e), 'status': '403'}, status=403)         
                 
                 
        else:
            return JsonResponse({'error': 'Only POST requests are allowed', 'status': '405'}, status=405)    
    except Exception as error:
        return JsonResponse({'message': 'Server Error', 'status': '500','error':error}, status=500)


@api_view(['POST'])
def delete_patient(request, patient_id):
    try:
        # Fetch the patient by patient_id
        patient = Patient_Registration.objects.get(id=patient_id)
        
        # Delete the patient
        patient.delete()
        
        # Return success response 
        return Response({
            "message": f"Patient with id {patient_id} has been deleted successfully."
        }, status=status.HTTP_200_OK)
    
    except Patient_Registration.DoesNotExist:
        # Return error response if patient does not exist
        return Response({
            "error": "Patient not found."
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        # Handle unexpected errors
        return Response({
            "error": f"An unexpected error occurred: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def schedule_appointment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            is_registered = data.get('is_registered', False)
            doctor_id = data.get('doctor')
            appointment_type = data.get('appointment_type')
            appointment_date = data.get('appointment_date')
            from_time = data.get('from_time')
            to_time = data.get('to_time')
            notes = data.get('notes')

            if is_registered:
                # Handle registered patient
                patient_id = data.get('patient_id')
                try:
                    patient = Patient_Registration.objects.get(patient_id=patient_id)
                except Patient_Registration.DoesNotExist:
                    return JsonResponse({'error': 'Patient ID not found', 'status': 404}, status=404)
            else:
                # Handle non-registered patient
                patient_name = data.get('patient_name')
                mobile_number = data.get('mobile_number')
                email = data.get('email')

                if not patient_name:
                    return JsonResponse({'error': 'Patient name is required for non-registered patients', 'status': 400}, status=400)

                if not mobile_number:
                    return JsonResponse({'error': 'Mobile number is required for non-registered patients', 'status': 400}, status=400)
                
                # Check if mobile number is already used
                if Patient_Registration.objects.filter(mobile_number=mobile_number).exists():
                    return JsonResponse({'error': 'Mobile number already in use', 'status': 400}, status=400)
                
                # Create a new non-registered patient
                patient = Patient_Registration.objects.create(
                    patient_name=patient_name,
                    mobile_number=mobile_number,
                    email=email,
                    is_registered=False  # Non-registered patients
                )

            # Fetch doctor details
            try:
                doctor = Staff_Allotment.objects.get(staff_id=doctor_id)
                doctor_metadata = Staff_MetaData.objects.get(staff_id=doctor_id)
            except Staff_Allotment.DoesNotExist:
                return JsonResponse({'error': 'Doctor not found', 'status': 404}, status=404)
            except Staff_MetaData.DoesNotExist:
                return JsonResponse({'error': 'Doctor metadata not found', 'status': 404}, status=404)

            # Create the appointment
            appointment = Patient_Appointment.objects.create(
                patient=patient.patient_id if is_registered else None,
                patient_name=patient.patient_name if not is_registered else None,
                mobile_number=mobile_number if not is_registered else None,
                email=email if not is_registered else None,
                doctor=doctor,
                appointment_type=appointment_type,
                appointment_date=appointment_date,
                from_time=from_time,
                to_time=to_time,
                notes=notes,
                is_registered=is_registered
            )

            # Prepare the response data
            response_data = {
                'appointment_id': appointment.appointment_id,
                'appointment_type': appointment.appointment_type,
                'appointment_date': appointment.appointment_date,
                'from_time': appointment.from_time,
                'to_time': appointment.to_time,
                'notes': appointment.notes,
                'patient_id': patient.patient_id if is_registered else None,
                'patient_name': patient.patient_name,  # Show patient_name for both registered and non-registered patients
                'doctor': doctor.staff_id,
                'doctor_name': doctor.username,
                'speciality': doctor_metadata.speciality,
                'is_registered': is_registered
            }

            return JsonResponse({
                'message': 'Appointment booked successfully',
                'data': response_data
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format', 'status': 400}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 500}, status=500)

    return JsonResponse({'error': 'Invalid request method', 'status': 405}, status=405)




@api_view(['POST'])
def rebook_appointment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            patient_id = data.get('patient_id')
            doctor_id = data.get('doctor')
            appointment_type = data.get('appointment_type')
            appointment_date = data.get('appointment_date')
            from_time = data.get('from_time')
            to_time = data.get('to_time')
            notes = data.get('notes')

            # Validate required fields
            if not patient_id:
                return JsonResponse({'error': 'Patient ID is required', 'status': 400}, status=400)

            if not doctor_id:
                return JsonResponse({'error': 'Doctor ID is required', 'status': 400}, status=400)

            # Check if the patient exists
            try:
                patient = Patient_Registration.objects.get(patient_id=patient_id)
            except Patient_Registration.DoesNotExist:
                return JsonResponse({'error': 'Patient ID not found', 'status': 404}, status=404)

            # Check if the doctor exists
            try:
                doctor = Staff_Allotment.objects.get(staff_id=doctor_id)
                doctor_metadata = Staff_MetaData.objects.get(staff_id=doctor_id)
            except Staff_Allotment.DoesNotExist:
                return JsonResponse({'error': 'Doctor not found', 'status': 404}, status=404)
            except Staff_MetaData.DoesNotExist:
                return JsonResponse({'error': 'Doctor metadata not found', 'status': 404}, status=404)

            # Check for existing appointment
            existing_appointment = Patient_Appointment.objects.filter(
                patient=patient_id,
                appointment_date=appointment_date,
                from_time=from_time,
                to_time=to_time,
                is_registered=True
            ).first()

            if existing_appointment:
                return JsonResponse({'error': 'An appointment with these details already exists', 'status': 400}, status=400)

            # Create the rebooked appointment
            appointment = Patient_Appointment.objects.create(
                patient=patient_id,
                doctor=doctor,
                appointment_type=appointment_type,
                appointment_date=appointment_date,
                from_time=from_time,
                to_time=to_time,
                notes=notes,
                is_registered=True
            )

            response_data = {
                'appointment_id': appointment.appointment_id,
                'appointment_type': appointment.appointment_type,
                'appointment_date': appointment.appointment_date,
                'from_time': appointment.from_time,
                'to_time': appointment.to_time,
                'notes': appointment.notes,
                'patient_id': patient_id,
                'patient_name': patient.patient_name,
                'doctor': doctor.staff_id,
                'doctor_name': doctor.username,
                'speciality': doctor_metadata.speciality,
                'is_registered': True
            }

            return JsonResponse({
                'message': 'Appointment rebooked successfully',
                'data': response_data
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format', 'status': 400}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 500}, status=500)

    return JsonResponse({'error': 'Invalid request method', 'status': 405}, status=405)

@api_view(['GET'])
def get_appointments(request):
    try:
        # Fetch all appointments
        appointments = Patient_Appointment.objects.all()

        # Prepare the response
        response_data = []
        for appointment in appointments:
            doctor = appointment.doctor
            doctor_metadata = Staff_MetaData.objects.filter(staff_id=doctor.staff_id).first()

            # Prepare appointment data
            appointment_data = {
                'appointment_id': appointment.appointment_id,
                'appointment_type': appointment.appointment_type,
                'appointment_date': appointment.appointment_date,
                'from_time': appointment.from_time,
                'to_time': appointment.to_time,
                'notes': appointment.notes,
                'doctor': doctor.staff_id,
                'doctor_name': doctor.username,
                'speciality': doctor_metadata.speciality if doctor_metadata and hasattr(doctor_metadata, 'speciality') else None,
                'is_registered': appointment.is_registered,
            }

            # Add patient details (registered or non-registered)
            if appointment.is_registered:
                patient = Patient_Registration.objects.get(patient_id=appointment.patient)
                appointment_data.update({
                    'patient_id': patient.patient_id,
                    'patient_name': patient.patient_name,
                })
            else:
                appointment_data.update({
                    'patient_id': None,
                    'patient_name': appointment.patient_name,
                })

            # Add appointment data to the response list
            response_data.append(appointment_data)

        # Return the response
        return JsonResponse({
            'appointments': response_data
        }, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e), 'status': 500}, status=500)


# def register_user(request):
#     try:
#         if request.method == 'POST':
#             data = json.loads(request.body)
#             print(data)
            
#             email = data.get('email')
#             username = data.get('username')
#             otp =data.get('otp')
#             mobile=data.get('mobile')
#             # fcm_token=data.get('fcm_token','null')
#             # print()


#             try:
#                 if email != '' and username != '' and otp != '' and mobile != '':
#                     # user=User.objects.get(email=email)
#                     exists = Patient.objects.filter(email=email).exists()
#                     print("exist :",exists)
#                     if exists:
#                         return JsonResponse({'message': 'Email already registered', 'status': '401'}, status=401)
                
#                     if Patient.objects.filter(username=username).exists():
#                         return JsonResponse({'message': 'Username already exists', 'status': '409'}, status=409)
                

#                     else:
#                         stored_otp=user_otp.objects.get(user_email=email)
#                         print("stored_otp :",stored_otp,otp)
#                         stored_otp=stored_otp.otp
#                         print("stored_otp :",stored_otp,otp)
#                         print(otp == stored_otp)
                        
#                         if(otp == stored_otp) :
#                             email = data.get('email')
#                             mobile = data.get('mobile')
#                             username = data.get('username')
                        

#                             # user = User.objects.create(email=email,registeredat=timezone.now(),username=username,mobile=mobile,fcm_token=fcm_token)
                        
#                             # user.save()
#                             user_otp.objects.filter(user_email=email).delete()

#                             user=user

#                             user_id=user
#                             print("user id",user_id)
#                             # wallets=wallet.objects.create(user_id=user_id,wallet_bal=100,email=user)
#                             # print("wallet :",wallets)
#                             # wallets.save()


                            
                            
                              
                        
#                             return JsonResponse({'message': 'User registered successfully', 'status': '200'}, status=200)
#                         else:
#                             return JsonResponse({'message': 'Entered Wrong OTP', 'status': '402'}, status=402)
#                 else:
#                     return JsonResponse({'message': 'Enter valid Details', 'status': '403'}, status=403)         
#             except Exception as e:
#                 return JsonResponse({'message': str(e), 'status': '403'}, status=403)         
                 
                 
#         else:
#             return JsonResponse({'error': 'Only POST requests are allowed', 'status': '405'}, status=405)    
#     except Exception as error:
#         return JsonResponse({'message': 'Server Error', 'status': '500','error':error}, status=500)
    

@api_view(['POST'])
def update_patient_details(request, patient_id):
    try:
        patient = Patient_Registration.objects.get(patient_id=patient_id)
    except Patient_Registration.DoesNotExist:
        return Response({
            "error": "Patient not found"
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        updated_data = {
            'patient_name': request.data.get('patient_name', patient.patient_name),
            'mobile_number': request.data.get('mobile_number', patient.mobile_number),
            'email': request.data.get('email', patient.email),
            'gender': request.data.get('gender', patient.gender),
            'address': request.data.get('address', patient.address),
            'date_of_birth': request.data.get('date_of_birth', patient.date_of_birth)
        }

        patient_serializer = PatientCreateSerializer(patient, data=updated_data, partial=True)
        if patient_serializer.is_valid():
            patient = patient_serializer.save()
            return Response({
                "message": "Patient details updated successfully",
                "patient": {
                    "patient_id": patient.patient_id,
                    "patient_name": patient.patient_name,
                    "mobile_number": patient.mobile_number,
                    "email": patient.email,
                    "gender": patient.gender,
                    "address": patient.address,
                    "date_of_birth": patient.date_of_birth,
                    "age": patient_serializer.data['age']
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "error": "Failed to update patient details",
            "details": patient_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_patient(request, patient_id):
    try:
        patient = Patient_Registration.objects.get(id=patient_id)  # Adjust 'id' if necessary
        patient_serializer = PatientCreateSerializer(patient)
        return Response({
            "patient": patient_serializer.data
        }, status=status.HTTP_200_OK)
    except Patient_Registration.DoesNotExist:
        return Response({
            "error": "Patient not found."
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "error": f"An unexpected error occurred: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
         
        
@api_view(['GET'])
def list_patients(request):
    patients = Patient_Registration.objects.all()
    serializer = PatientCreateSerializer(patients, many=True)
    return Response({
        "patients": serializer.data
    }, status=status.HTTP_200_OK)       


@api_view(['POST'])
def registerPatientNow(request):
    try:
        # Collect the patient data from the request
        patient_data = {
            'patient_name': request.data.get('patient_name'),
            'mobile_number': request.data.get('mobile_number'),
            'email': request.data.get('email'),
            'gender': request.data.get('gender'),
            'address': request.data.get('address'),
            'date_of_birth': request.data.get('date_of_birth'),
            'is_registered': True
        }

        with transaction.atomic():
            # Create a new patient serializer instance
            patient_serializer = PatientCreateSerializer(data=patient_data)
            
            # Validate the data
            if patient_serializer.is_valid():
                # Save the patient if data is valid
                patient = patient_serializer.save()
                return Response({
                    "status": "Success",
                    "message": "Patient registered successfully",
                    "patient": {
                        "patient_id": patient.patient_id,
                        "patient_name": patient.patient_name,
                        "mobile_number": patient.mobile_number,
                        "email": patient.email,
                        "gender": patient.gender,
                        "address": patient.address,
                        "date_of_birth": patient.date_of_birth,
                    }
                }, status=status.HTTP_201_CREATED)
            else:
                # Return validation errors
                return Response({
                    "status": "Failed",
                    "message": "Patient registration failed",
                    "details": patient_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Handle any unforeseen errors and return an appropriate message
        return Response({
            "status": "Failed",
            "message": "An error occurred during patient registration",
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)