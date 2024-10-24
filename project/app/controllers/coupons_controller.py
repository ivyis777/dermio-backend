import json
from decimal import Decimal
from django.http import JsonResponse
from django.utils import timezone

from app.models.misc import Coupons
from app.serializers import CouponsSerializer





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


from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


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