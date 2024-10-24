
from datetime import timedelta
import json
import random
import string
# from time import timezone
from django.utils import timezone


from django.http import JsonResponse
from app.models.patient_models import Patient
from app.models.email_models import user_otp

from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
# import json
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from app.models.notifications_models import Notification

def create_notification(to_user_id,Title,message):
    print("in create notification")
    try:
        user = Patient.objects.get(id=to_user_id)
        notification_object_create=Notification.objects.create(user_id=user,
                                                            title=Title,
                                                            message=message)
    except Exception as error:
        return JsonResponse ({"error":str(error),"status" :"400"},status=400)

def generate_random_otp():
        characters =  string.digits
        return ''.join(random.choice(characters) for _ in range(4))



@csrf_exempt
def send_otp_email(subject, body, recipient):
            try:
                send_mail(subject, body, 'kwiizzapp@gmail.com', [recipient])
                return True
            except Exception as e:
                print(f"Error sending email: {str(e)}")
                return False


def send_otp(request):
    try:
        # Parse and validate request
        data = json.loads(request.body)
        recipient = data.get('email')
        purpose = data.get('purpose')
        
        if not recipient or not purpose:
            return JsonResponse({'message': 'Email and purpose are required', 'status': '400'}, status=400)
        
        otp = generate_random_otp()  # Assuming this function generates a random OTP
        print("Generated OTP:", otp)

        # Helper function to send OTP email
        
            
        otp_exist=user_otp.objects.filter(user_email=recipient,purpose=purpose).exists()
        print("otp exists : ")
        
        
        # Handle different purposes
        if purpose == 'signup':
            exists = Patient.objects.filter(email=recipient).exists()
            if exists:
                return JsonResponse({'message': 'Email already registered', 'status': '401'}, status=401)
            if not send_otp_email("Your One-Time Password (OTP) for Signup", f"Your Signup OTP is: {otp}", recipient):
                
                return JsonResponse({'message': 'Failed to send OTP email', 'status': '500'}, status=500)
            if otp_exist:

                user=user_otp.objects.get(user_email=recipient,purpose=purpose)
                user.otp=otp
                user.save()
                return JsonResponse({'message': 'OTP has been sent to your email', 'status': '200'}, status=200)


            else:
                otp_save=user_otp.objects.create(user_email=recipient,otp=otp,purpose=purpose,delete_at=timezone.now() + timedelta(minutes=1))
                
                return JsonResponse({'message': 'OTP has been sent to your email', 'status': '200'}, status=200)

        elif purpose == 'login':
            if not send_otp_email("Your One-Time Password (OTP) for Login", f"Your login OTP is: {otp}", recipient):
                return JsonResponse({'message': 'Failed to send OTP email', 'status': '500'}, status=500)

            print(otp_exist)
            if otp_exist:

                user=user_otp.objects.get(user_email=recipient,purpose=purpose)
                user.otp=otp
                user.save()
                return JsonResponse({'message': 'OTP has been sent to your email', 'status': '200'}, status=200)

            else:
                otp_save=user_otp.objects.create(user_email=recipient,otp=otp,purpose=purpose,delete_at=timezone.now() + timedelta(minutes=1))
                return JsonResponse({'message': 'OTP has been sent to your email', 'status': '200'}, status=200)

        elif purpose == 'resend':
            

            if not send_otp_email("Your One-Time Password (OTP) for Resend OTP", f"Your Resend OTP is: {otp}", recipient):
                return JsonResponse({'message': 'Failed to send OTP email', 'status': '500'}, status=500)
            if otp_exist:

                user=user_otp.objects.get(user_email=recipient,purpose=purpose)
                user.otp=otp
                user.save()
                return JsonResponse({'message': 'OTP has been sent to your email', 'status': '200'}, status=200)

            else:
                otp_save=user_otp.objects.create(user_email=recipient,otp=otp,purpose=purpose)
                return JsonResponse({'message': 'OTP has been resent to your email', 'status': '200'}, status=200)

        else:
            return JsonResponse({'message': 'Invalid purpose', 'status': '400'}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON format', 'status': '400'}, status=400)
    except KeyError as ke:
        return JsonResponse({'message': f'Missing key: {str(ke)}', 'status': '400'}, status=400)
    except ValidationError as ve:
        return JsonResponse({'message': f'Invalid data: {str(ve)}', 'status': '400'}, status=400)
    except IntegrityError as ie:
        return JsonResponse({'message': 'Database error', 'status': '500'}, status=500)
    except Exception as error:
        # Log the error if necessary
        print(f"Unexpected error: {str(error)}")
        return JsonResponse({'message': 'An unexpected error occurred', 'status': '500'}, status=500)

# Helper function to validate email format
# import re
# def validate_email_format(email):
#     regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#     return re.match(regex, email)

# def send_otp(request):
#     try:
#         print(request)
#         data = json.loads(request.body)
#         print(data)
#         recipient=data.get('email')
#         purpose=data.get('for')
#         print(recipient)

#         otp = generate_random_otp()
#         print("Generated OTP:", otp)



#         if purpose == 'signup':
#             exists = Patient.objects.filter(email=recipient).exists()
#             print("user exists : ",exists)
#             if exists:                    
#                 return JsonResponse({'message': 'Email already registered', 'status': '401'}, status=401)
#             send_mail("Your One-Time Password (OTP) for Signup", f"Your Signup OTP is: {otp}", 'kwiizzapp@gmail.com', recipient)
#             return JsonResponse({'message': 'Otp has resent to your mail', 'status': '200'}, status=200)
#         elif purpose == 'login':
#             send_mail("Your One-Time Password (OTP) for Login", f"your login OTP is: {otp}", 'kwiizzapp@gmail.com', recipient)
#             return JsonResponse({'message': 'Otp has resent to your mail', 'status': '200'}, status=200)
#         elif purpose=='resend':

#             send_mail("Your One-Time Password (OTP) for Resend OTP", f"Your Resend OTP is: {otp}", 'kwiizzapp@gmail.com', recipient)
#             return JsonResponse({'message': 'Otp has resent to your mail', 'status': '200'}, status=200)
#     except Exception as error :
#             return JsonResponse({'error': str(error), 'status': '500'}, status=500)
         
         
    
         
         
         


    # exists=user_otp.objects.filter(user_email=recipient).exists()
    # exists=user_otp.objects.filter(user_email=recipient).exists()
    # print("Exist :",exists)


    # if exists:
    #     recipient_email=[recipient]
    #     user=user_otp.objects.get(user_email=recipient)
    #     print(user)
    #     otp=user.otp
    #     print(otp,recipient_email)
        
    
    #     send_mail("Your One-Time Password (OTP)", f"Your OTP is: {otp}", 'kwiizzapp@gmail.com', recipient_email)
    #     return JsonResponse({'message': 'Otp has resent to your mail', 'status': '200'}, status=200)
    # else:
    #      return JsonResponse ({"message":"Otp not sent Please Try Again","status":"401"},status=401)



@csrf_exempt
def signup_otp(request):
    print(request)
    data = json.loads(request.body)
    print(data)
    recipient=data.get('email')
    print(recipient,type(recipient))
    # user=User.objects.get(email=recipient).exists

    exists = Patient.objects.filter(email=recipient).exists()
    print("user exists : ",exists)
    if exists:                    
            return JsonResponse({'message': 'Email already registered', 'status': '401'}, status=401)
    # except: 
    else:
        print("in except")
        otp = generate_random_otp()

        recipient_email=[recipient]

        otp_exists=user_otp.objects.filter(user_email=recipient).exists()
        print(exists)
        if otp_exists:
            print("Generated OTP:", otp)

            user=user_otp.objects.get(user_email=recipient)
            user.otp=otp

            user.save()
            return JsonResponse({'message': 'Email OTP sent successfully',
                                 "status":"200"},status=200)
        else:            
            print("Generated OTP:", otp)
            otp_save=user_otp.objects.create(user_email=recipient,otp=otp,created_at=timezone.now())
            send_mail("Email OTP to Sign-Up", f"{otp} to Sign-Up Kwiizz app", 'kwiizzapp@gmail.com', recipient_email)
            return JsonResponse({'message': 'Email sent successfully',"status":"200"},status=200)