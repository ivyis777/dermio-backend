import json
import time
from app.models.Staff_models import *
from rest_framework.decorators import api_view
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models.misc import *
from app.models.wallet_models import *
from app.controllers.wallet_controller import wallet

from rest_framework import generics
# from .models import Staff_MetaDatas
from app.serializers import StaffMetaDataSerializer,TopDoctorsSerializer,SlotSerializer



from app.models.Staff_models import Slot
from datetime import timedelta, time, datetime
# from .models import Slot, Doctor


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from .models import Staff_MetaData
# from .serializers import StaffMetaDataSerializer
from datetime import time, date
from datetime import datetime, timedelta
from django.db.models import Q

def generate_time_slots(doctor, date, start_time, end_time, slot_duration=15):
    """
    Generate 15-minute interval time slots for a given date and time range.
    """
    slots = []
    current_time = start_time
    print("current time : ",current_time)

    while current_time < end_time:
        next_time = (datetime.combine(date, current_time) + timedelta(minutes=slot_duration)).time()
        if next_time > end_time:  # Ensure we don't go beyond the doctor's end time
            break

        # Create and save a new TimeSlot for each interval
        slot = Slot.objects.create(
            doctor=doctor,
            date=date,
            start_time=current_time,
            end_time=next_time,
            is_available=True,
            on_leave=False    # Initially, the slot is not booked
        )
        slots.append(slot)
        current_time = next_time
    
    # print("slots : ",slots)
    return slots


@api_view(['POST'])
def check_availability(request):

    # print("Entered check availability API")
    
    try:
        # Parse the request data
        data = json.loads(request.body)
        staff_id = data.get('staff_id')
        date_str = data.get("date")  # Expecting a date in ISO format like "2024-12-30"
        start_time_str = data.get("start_time")  # This should be a string like "09:00"
        end_time_str = data.get("end_time")  # This should be a string like "17:00"

        # Convert date string to a date object
        try:
            slot_date = date.fromisoformat(date_str)  # Convert the date string to a `date` object
        except ValueError:
            return JsonResponse({"error": "Invalid date format. Please use ISO format (YYYY-MM-DD)."}, status=400)

        # Parse start_time and end_time
        try:
            start_time = time.fromisoformat(start_time_str) if start_time_str else time(9, 0)
            end_time = time.fromisoformat(end_time_str) if end_time_str else time(17, 0)
        except ValueError:
            return JsonResponse({"error": "Invalid time format. Please use ISO time format (HH:MM)."}, status=400)


        # Fetch the doctor/staff details
        doctor = Staff_Allotment.objects.get(staff_id=staff_id)
        # print("1")
        # Check if the doctor has a leave during the requested date and time range
        leave_exists = Leave_Management.objects.filter(
            Q(start_time__lte=end_time) & Q(end_time__gte=start_time),
            staff_id=doctor,
            date=slot_date,
            ).exists()
        
        # print("2")
        # doctor=Staff_MetaData.objects.get(staff_id=staff_id)
        # Query the slots for the given date
        queryset = Slot.objects.filter(doctor=staff_id, date=slot_date)
        serializer = SlotSerializer(queryset, many=True)
        data = serializer.data
        # print("data :",data)
        doctor = Staff_Allotment.objects.get(staff_id=staff_id)

        # print("3")
        # If no slots exist, generate slots dynamically
        if not serializer.data:
            print("null serializer")
            data = generate_time_slots(doctor, slot_date, start_time, end_time, slot_duration=15)
        # print("slots : ",data)

        return JsonResponse({"message":"Slots created successfully", "status": "200"}, status=200)
    except Exception as e:
        return JsonResponse({'message': str(e), 'status': '403'}, status=403) 



    

@api_view(['GET'])
def get_staff_by_department(request):
    print("dept ",request.query_params.get('department', None))
    departments = request.query_params.get('department', None)  # Get department from query params

    print("department : ",departments,type(departments))
    print(departments,"Cardiology",departments=="Cardiology")

    if departments is None:
        return Response({"error": "Department parameter is required","status":"400"}, status=400)
 
    # Filter staff by department
    staff_metadata = Staff_MetaData.objects.filter(department=departments)  # case-insensitive filter
    print(staff_metadata)
    if not staff_metadata.exists():
        return Response({"message": "No staff found in the given department","status":"400"}, status=400)

    # Serialize the data
    serializer = StaffMetaDataSerializer(staff_metadata, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



def get_available_slots(doctor, date):
    booked_slots = Slot.objects.filter(doctor=doctor, date=date)
    booked_times = [(slot.start_time, slot.end_time) for slot in booked_slots]

    start_time = doctor.start_time
    end_time = doctor.end_time
    slot_duration = timedelta(minutes=doctor.slot_duration)

    available_slots = []
    current_time = datetime.combine(date, start_time)
    end_time_combined = datetime.combine(date, end_time)

    while current_time + slot_duration <= end_time_combined:
        slot_start = current_time.time()
        slot_end = (current_time + slot_duration).time()

        # Check if this slot is already booked
        if (slot_start, slot_end) not in booked_times:
            available_slots.append({
                'start_time': slot_start,
                'end_time': slot_end,
                'is_available': True
            })

        current_time += slot_duration

    return available_slots




class AvailableSlotsView(APIView):
    def get(self, request, doctor_id, date):
        doctor = Staff_Allotment.objects.get(staff_id=doctor_id)
        available_slots = get_available_slots(doctor, date)
        return Response(available_slots)

# class StaffMetaDataUpdateView(APIView):
#     def post(self, request, staff_meta_id):
#         try:
#             staff_meta = Staff_MetaData.objects.get(staff_meta_id=staff_meta_id)
#         except Staff_MetaData.DoesNotExist:
#             return Response({"error": "Staff MetaData not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = StaffMetaDataSerializer(staff_meta, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])

class StaffMetaDataUpdateOrCreateView(APIView):
    def post(self, request, staff_meta_id=None):
        # Check if staff_meta_id is provided (for update)
        if staff_meta_id:
            try:
                staff_meta = Staff_MetaData.objects.get(staff_meta_id=staff_meta_id)
            except Staff_MetaData.DoesNotExist:
                # If not found, proceed with creating a new entry
                staff_meta = None
        else:
            # No staff_meta_id passed, so we are creating a new record
            staff_meta = None

        # Use the serializer to validate and save data (create if not found)
        serializer = StaffMetaDataSerializer(staff_meta, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if staff_meta:
                # Return an update response
                return Response({
                    "status": 200,
                    "message": "Staff MetaData updated successfully",
                    "data": serializer.data
                })
            else:
                # Return a creation response
                return Response({
                    "status": 201,
                    "message": "Staff MetaData created successfully",
                    "data": serializer.data
                })

        # Return validation errors
        return Response({
            "status": 400,
            "message": "Invalid data",
            "errors": serializer.errors
        })


class TopDoctorsListView(generics.ListCreateAPIView):
    queryset = Top_doctors.objects.all()
    serializer_class = TopDoctorsSerializer


class StaffMetaDataByDesignationView(generics.ListAPIView):
    serializer_class = StaffMetaDataSerializer

    def get_queryset(self):
        designation = self.kwargs['profession']
        return Staff_MetaData.objects.filter(profession=designation)


def get_meta_data():
    pass



@api_view(['GET'])
def get_all_staff_users_with_metadata(request):
    try:
        users = Staff_Allotment.objects.all()
        users_data = []
        
        for user in users:
            user_data = {
                "staff_id": user.staff_id,
                "username": user.username,
                "mobile_number": user.mobile_number,
                "email": user.email,
                "is_admin": user.is_admin,
                "is_nurse": user.is_nurse,
                "is_doctor": user.is_doctor,
                "is_pharmacist": user.is_pharmacist,
                "is_receptionist": user.is_receptionist,
                "status": user.status,
            }
            
            # Fetch related metadata
            metadata = Staff_MetaData.objects.filter(staff_id=user.staff_id).first()
            if metadata:
                metadata_data = {
                    "name": metadata.name,
                    "gender": metadata.gender,
                    "date_of_birth": metadata.date_of_birth,
                    "age": metadata.age,
                    "registration_number": metadata.registration_number,
                    "consulting_fee": str(metadata.consulting_fee),
                    "permanent_address": metadata.permanent_address,
                    "speciality": metadata.speciality,
                    "designation": metadata.designation
                }
                user_data['metadata'] = metadata_data
            else:
                user_data['metadata'] = None  # If no metadata found
            
            users_data.append(user_data)

        return JsonResponse({"users": users_data, "status": "200"})
    except Exception as error:
        return JsonResponse({"Error": str(error), "status": "500"})



@api_view(['POST'])
@csrf_exempt
def update_user_reg(request):
    try:
        # Parse the incoming data
        data = json.loads(request.body)
        staff_id = data.get('staff_id')

        if not staff_id:
            return JsonResponse({'error': 'staff_id is required', 'status': 400}, status=400)

        # Fetch the existing Staff_Allotment object using staff_id
        try:
            user_object = Staff_Allotment.objects.get(staff_id=staff_id)
        except Staff_Allotment.DoesNotExist:
            return JsonResponse({'error': 'User not found', 'status': 404}, status=404)

        # Update fields in Staff_Allotment
        username = data.get('username', user_object.username)
        is_admin = data.get('is_admin', user_object.is_admin)
        is_nurse = data.get('is_nurse', user_object.is_nurse)
        is_doctor = data.get('is_doctor', user_object.is_doctor)
        is_receptionist = data.get('is_receptionist', user_object.is_receptionist)
        is_pharmacist = data.get('is_pharmacist', user_object.is_pharmacist)
        mobile_number = data.get('mobile_number', user_object.mobile_number)
        email = data.get('email', user_object.email)

        # Update Staff_Allotment object
        user_object.username = username
        user_object.is_admin = is_admin
        user_object.is_nurse = is_nurse
        user_object.is_doctor = is_doctor
        user_object.is_receptionist = is_receptionist
        user_object.is_pharmacist = is_pharmacist
        user_object.mobile_number = mobile_number
        user_object.email = email
        user_object.save()

        # Update Staff_MetaData object if it exists
        try:
            staff_metadata = Staff_MetaData.objects.get(staff_id=user_object)
            # Update metadata fields based on role
            if is_doctor:
                staff_metadata.name = data.get('name', staff_metadata.name)
                staff_metadata.speciality = data.get('speciality', staff_metadata.speciality)
                staff_metadata.designation = data.get('designation', staff_metadata.designation)
                staff_metadata.registration_number = data.get('registration_number', staff_metadata.registration_number)
                staff_metadata.consulting_fee = data.get('consulting_fee', staff_metadata.consulting_fee)
                staff_metadata.permanent_address = data.get('permanent_address', staff_metadata.permanent_address)
                staff_metadata.age = data.get('age', staff_metadata.age)
                staff_metadata.date_of_birth = data.get('date_of_birth', staff_metadata.date_of_birth)
                staff_metadata.gender = data.get('gender', staff_metadata.gender)
                
                
            elif is_nurse or is_pharmacist or is_receptionist:
                staff_metadata.name = data.get('name', staff_metadata.name)
                staff_metadata.age = data.get('age', staff_metadata.age)
                staff_metadata.gender = data.get('gender', staff_metadata.gender)
                staff_metadata.designation = data.get('designation', staff_metadata.designation)
                staff_metadata.permanent_address = data.get('permanent_address', staff_metadata.permanent_address)
            staff_metadata.save()
        except Staff_MetaData.DoesNotExist:
            # Handle if metadata doesn't exist for the user
            pass

        # Return the updated user data
        return JsonResponse({
            "message": "User data updated successfully",
            "status": 200,
            "user_data": {
                "staff_id": user_object.staff_id,
                "username": user_object.username,
                "email": user_object.email,
                "mobile_number": user_object.mobile_number,
                "role": {
                    "is_doctor": user_object.is_doctor,
                    "is_nurse": user_object.is_nurse,
                    "is_admin": user_object.is_admin,
                    "is_receptionist": user_object.is_receptionist,
                    "is_pharmacist": user_object.is_pharmacist
                }
            }
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format', 'status': 400}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e), 'status': 500}, status=500)







