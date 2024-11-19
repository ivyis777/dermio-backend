
from app.models.notifications_models import Notification
from app.serializers import NotificationSerializer
from rest_framework.views import APIView
import json
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.db.models import Q
from app.models.patient_models import Patient


def create_notification(to_user_id,Title,message):
    print("in create notification")
    try:
        patient = Patient.objects.get(id=to_user_id)
        notification_object_create=Notification.objects.create(user_id=patient,
                                                            title=Title,
                                                            message=message)
    except Exception as error:
        return JsonResponse ({"error":str(error),"status" :"400"},status=400)



class NotificationList(APIView):

    def get(self, request,pk, *args, **kwargs):

        patient = request.user

        try:
            # data=json.loads(request.body)
            print("pk : ",pk)
            queryset = Notification.objects.filter(Q(user_id=pk) | Q(user_id__isnull=True)).order_by('id')
            print(queryset)
            # serializer_class = NotificationSerializer
            print("pk : ",pk)

            # queryset = self.filter_queryset(self.get_queryset())
            serializer = NotificationSerializer(queryset, many=True)
            print("pk : ",pk)
            
            return Response(serializer.data, status="200")
        
        except ParseError as e:
            # Handle JSON parsing errors
            return JsonResponse({"errors": str(e)}, status="400")
        
        except Exception as e:
            # Handle any other exceptions
            return JsonResponse({"errors": str(e)}, status="500")