from django.http import JsonResponse
from rest_framework.decorators import api_view

from app.models.wallet_models import wallet
from app.models.patient_models import Patient
import json

@api_view(['POST'])
# @csrf_exempt
def wallet_bal(request):
    try:
        data = json.loads(request.body)
        patient_id = data.get('user_id')
        # print(data,type(user_id))


        if not patient_id :
            return JsonResponse({"error": "User ID is required", "status": "400"})
        
        exists=Patient.objects.filter(id=patient_id).exists()
        if not exists:
            return JsonResponse({"error": "User ID is not registered", "status": "401"})


        user= wallet.objects.filter(user_id=patient_id).first()

        if user:
            return JsonResponse({"Wallet balance": float(user.wallet_bal),"status": "200"})
            
            # return JsonResponse({"Wallet balance": float(user.wallet_bal),"Debits":serializer_debit.data,"Credits":serializer_credit.data ,"status": "200"})
        else:
            return JsonResponse({"message": "User does not exist", "status": "404"})
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format", "status": "402"})

    except Exception as error:
        return JsonResponse({"error": str(error), "status": "500"})
