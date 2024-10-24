# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.models.misc import Promotions
from app.serializers import PromotionsSerializer

# Get all promotions or create a new promotion

@api_view(['GET','POST'])

def promotions_list(request):
    if request.method == 'GET':
        # Retrieve all promotions
        promotions = Promotions.objects.all()
        serializer = PromotionsSerializer(promotions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new promotion with image upload
        serializer = PromotionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a single promotion
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def promotions_detail(request, promotion_id):
    try:
        promotion = Promotions.objects.get(promotion_id=promotion_id)
    except Promotions.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Return a single promotion
        serializer = PromotionsSerializer(promotion)
        return Response(serializer.data)

    elif request.method == 'PUT' or request.method == 'PATCH':
        # Update an existing promotion
        serializer = PromotionsSerializer(promotion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the promotion
        promotion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)