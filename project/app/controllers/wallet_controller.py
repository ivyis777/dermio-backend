from django.http import JsonResponse
from rest_framework.decorators import api_view

from app.models.wallet_models import*
from app.models.patient_models import Patient
import json
from app.serializers import WalletTranSerializer_credit,WalletTranSerializer_debit

@api_view(['POST'])
# @csrf_exempt
def wallet_bal(request):
    try:
        data = json.loads(request.body)
        patient_id = data.get('patient_id')
        # print(data,type(user_id))


        if not patient_id :
            return JsonResponse({"error": "User ID is required", "status": "400"})
        
        exists=Patient.objects.filter(id=patient_id).exists()
        if not exists:
            return JsonResponse({"error": "User ID is not registered", "status": "401"})


        user= wallet.objects.filter(patient_id=patient_id).first()

        user_transaction_debit=wallet_transactions_debit.objects.filter(patient_id=patient_id)
        # user_id=User.objects.get(id=user_id)
        # print(user_id,1)
        
        serializer_debit=WalletTranSerializer_debit(user_transaction_debit,many=True)
        # print(serializer_debit.data)
        user_transaction_credit=wallet_transactions_credit.objects.filter(to_user_id=user.patient_id)
        # print(ser)

        serializer_credit=WalletTranSerializer_credit(user_transaction_credit,many=True)
        # print(serializer_credit.data,2)

        if user:
            # return JsonResponse({"Wallet balance": float(user.wallet_bal),"status": "200"})
            
            return JsonResponse({"Wallet balance": float(user.wallet_bal),"Debits":serializer_debit.data,"Credits":serializer_credit.data ,"status": "200"})
        else:
            return JsonResponse({"message": "User does not exist", "status": "404"})
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format", "status": "402"})

    except Exception as error:
        return JsonResponse({"error": str(error), "status": "500"})
