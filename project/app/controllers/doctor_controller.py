from django.http import JsonResponse 
from app.models.Staff_models import *
from django.views.decorators.csrf import csrf_exempt





@csrf_exempt
def get_doctor_profiles(request):
    if request.method == 'GET':
        try:
            # Query all doctors from the Staff_Allotment table
            doctors = Staff_Allotment.objects.filter(is_doctor=True)
            
            # If no doctors found, return an appropriate message
            if not doctors.exists():
                return JsonResponse({'message': 'No doctors found', 'status': 404}, status=404)

            # Prepare doctor profile data
            doctor_profiles = []
            for doctor in doctors:
                # Fetch metadata for each doctor (if applicable)
                metadata = Staff_MetaData.objects.filter(staff_id=doctor).first()

                # Add basic details along with metadata if available
                doctor_profiles.append({
                    'staff_id': doctor.staff_id,  # Include staff_id in the response
                    'doctor_id': doctor.staff_id,  # Include doctor_id in the response (same as staff_id)
                    'username': doctor.username,
                    'email': doctor.email,
                    'mobile_number': doctor.mobile_number,
                    'status': doctor.status,
                    'metadata': {
                        'staff_meta_id': metadata.staff_meta_id if metadata else None,
                        'name': metadata.name if metadata else None,
                        'gender': metadata.gender if metadata else None,
                        'date_of_birth': metadata.date_of_birth if metadata else None,
                        'age': metadata.age if metadata else None,
                        'registration_number': metadata.registration_number if metadata else None,
                        'consulting_fee': metadata.consulting_fee if metadata else None,
                        'permanent_address': metadata.permanent_address if metadata else None,
                        'speciality': metadata.speciality if metadata else None,
                        'designation': metadata.designation if metadata else None,
                        
                    } if metadata else None,
                })

            return JsonResponse({'message': 'Doctors retrieved successfully', 'data': doctor_profiles, 'status': 200}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 500}, status=500)

    return JsonResponse({'error': 'Invalid request method', 'status': 405}, status=405)
