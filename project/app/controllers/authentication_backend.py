from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model



from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# @method_decorator(csrf_exempt, name='post')
# class JWTAuthenticationBackend(BaseBackend):
#     def authenticate(self, request, user_id=None):
#         print("user_id in authentication",user_id)
#         print("in Authentication")
#         if user_id is None:
#             return None
 
#         User = get_user_model()
#         try:
#             print("in try")
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         User = get_user_model()
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None

import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model

from app.models.patient_models import Patient

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print("in authenticate :")
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            print("IN AUTHENTICATE TRY : ",settings.SECRET_KEY)

            token = auth_header.split(' ')[1]  # Split "Bearer <token>"

            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            patient_id = decoded_token.get('patient_id')
            print("USER_ID :",patient_id)

            if not patient_id:
                raise AuthenticationFailed('Invalid token')

            # User = get_user_model()
            user = Patient.objects.get(pk=patient_id)
            print("Iam here :",user)
            return (user, None)  # Return a tuple of (user, None)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        # except User.DoesNotExist:
        #     raise AuthenticationFailed('User not found')