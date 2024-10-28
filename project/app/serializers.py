from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from app.models.Staff_models import *
from app.models.misc import *
from app.models.patient_models import*


from app.models.notifications_models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'timestamp']

class PatientSymptomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient_Symptoms
        fields = ['symptom_id', 'symptom_name']



from app.models.patient_models import Spotted_Images,Book_Appointment

class SpottedImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spotted_Images
        fields = ['spotted_place', 'image_1', 'image_2']

class BookAppointmentSerializer(serializers.ModelSerializer):
    spotted_data = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )

    class Meta:
        model = Book_Appointment
        fields = '__all__'

    def create(self, validated_data):

        doctor_id = validated_data.get('doctor_id')
        appointment_date = validated_data.get('appointment_date')
        slot_id = validated_data.get('slot_id')
        slot_id=slot_id.slot_id

        print("doctor_id :",doctor_id ,"appointment_date :",appointment_date ,"slot_id :",slot_id)

        doctor = validated_data.get('doctor_id', None)
        print("doctor :",doctor)
        if doctor is None:
            # Handle case if doctor_id is not provided
            raise serializers.ValidationError({'doctor_id': 'This field is required.'})
        
        try:
            slot = Slot.objects.get(slot_id=slot_id)
            print("available :",slot.is_available)
            if not slot.is_available:
                raise serializers.ValidationError({'slot_id': 'This slot is not available.'})
        except Slot.DoesNotExist:
            raise serializers.ValidationError({'slot_id': 'This slot does not exist.'})
        
        # Pop spotted_data from the validated data
        spotted_data = validated_data.pop('spotted_data', [])
        print("spotted_data :",spotted_data)
        
        # Create the appointment
        appointment = Book_Appointment.objects.create(**validated_data)
        print("appointment")
        
        # Loop through the spotted_data and create each Spotted_Images object
        for spot in spotted_data:
            Spotted_Images.objects.create(
                Appointment_id=appointment.appointment_id,
                spotted_place=spot.get('spotted_place'),
                image_1=spot.get('image_1'),
                image_2=spot.get('image_2')
            )
        
        slot.is_available = False
        slot.save()
        
        return appointment

# class BookAppointmentSerializer(serializers.ModelSerializer):
#     print("entered book appoinment")
#     spotted_images = SpottedImagesSerializer(many=True)  # Nested serializer for multiple images

#     class Meta:
#         model = Book_Appointment
#         fields =  [
#             'appointment_id', 'doctor_id', 'appointment_date', 'slot_id', 'age',
#             'blood_group', 'relation', 'description', 'symptoms', 'total_amount',
#             'coupon_used', 'coupon_amount', 'net_payable', 'spotted_images'
#         ]

#     def create(self, validated_data):
#         print("entered create :",validated_data)

#         # Extract spotted images data from request
#         spotted_images_data = self.context['request'].FILES.getlist('spotted_images')
#         # spotted_images_data = validated_data.pop('spotted_images',[])
#         print("spotted image data :",spotted_images_data)
#         # Create appointment
#         appointment = Book_Appointment.objects.create(**validated_data)
#         print("before for loop :",appointment)

#         # Create each spotted image and associate it with the appointment
#         for image_data in spotted_images_data:
#             Spotted_Images.objects.create(appointment=appointment, **image_data)

#         return appointment

#     def update(self, instance, validated_data):
#         # Extract spotted images data from request
#         spotted_images_data = validated_data.pop('spotted_images')
#         # Update appointment details
#         instance.doctor_id = validated_data.get('doctor_id', instance.doctor_id)
#         instance.appointment_date = validated_data.get('appointment_date', instance.appointment_date)
#         instance.slot_id = validated_data.get('slot_id', instance.slot_id)
#         instance.age = validated_data.get('age', instance.age)
#         instance.blood_group = validated_data.get('blood_group', instance.blood_group)
#         instance.relation = validated_data.get('relation', instance.relation)
#         instance.description = validated_data.get('description', instance.description)
#         instance.symptoms = validated_data.get('symptoms', instance.symptoms)
#         instance.total_amount = validated_data.get('total_amount', instance.total_amount)
#         instance.coupon_used = validated_data.get('coupon_used', instance.coupon_used)
#         instance.coupon_amount = validated_data.get('coupon_amount', instance.coupon_amount)
#         instance.net_payable = validated_data.get('net_payable', instance.net_payable)
#         instance.save()

#         # Handle the spotted images update or creation
#         for image_data in spotted_images_data:
#             image_id = image_data.get('image_id')
#             if image_id:
#                 # Update existing image
#                 spotted_image = Spotted_Images.objects.get(pk=image_id, appointment=instance)
#                 spotted_image.spotted_place = image_data.get('spotted_place', spotted_image.spotted_place)
#                 spotted_image.image_1 = image_data.get('image_1', spotted_image.image_1)
#                 spotted_image.image_2 = image_data.get('image_2', spotted_image.image_2)
#                 spotted_image.save()
#             else:
#                 # Create new spotted image
#                 Spotted_Images.objects.create(appointment=instance, **image_data)

#         return instance


class CouponsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupons
        fields = '__all__'

# serializers.py
from rest_framework import serializers



# from .models import Promotions


from rest_framework import serializers


# from  import Staff_MetaData


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'

class PromotionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotions
        fields = ['promotion_id', 'url', 'image']   # Include fields you want to expose



class TopDoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Top_doctors
        fields = '__all__'  # You can also specify specific fields like ['top_doctor_id', 'doctor_id', 'department', 'image']



class StaffMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff_MetaData
        fields = '__all__' 

# from .models import (
#                      Staff_Allotment,
#                      Staff_MetaData,
#                     #  Patient_Metadata
#                     Patient_Appointment,
#                     Patient_Registration
#                      )
from app.models.patient_models import Patient_Appointment,Patient_Registration,Patient
from app.models.Staff_models import Staff_Allotment,Staff_MetaData



class PatientUpdateSerializer(serializers.ModelSerializer):
    
    # image = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['id', 'name', 'gender', 'email', 'mobile', 'address', 'city', 'country', 'state', 'pincode', 'image','age',"username"]
        
        # def get_image(self, user):
        #     if user.image:
        #         path=user.image
        #         path1=user.image.url
        #         print(path1)
        #         converted_string = path1.replace("/app.images/", "/user_images/")
        #         print(converted_string)
                
                
                
            #     print("iam in image function",user.image.url,path1,type(path1))
            #     return converted_string
            # return None
# from app.models
# from app.models

                     
                     
# class StaffSerializer(serializers.ModelSerializer):
#     metadata = serializers.SerializerMethodField()
#     role = serializers.SerializerMethodField()
#     # clinic_id = serializers.SerializerMethodField()
#     # branch_id = serializers.SerializerMethodField()

#     class Meta:
#         model = Staff_Allotment
#         fields = ['staff_id', 'username', 'email', 'mobile_number', 'role', 'metadata']

#     def get_metadata(self, obj):
#         # Fetch the associated metadata for the staff
#         try:
#             staff_metadata = Staff_MetaData.objects.get(staff_id=obj.staff_id)
#         except Staff_MetaData.DoesNotExist:
#             return {}

#         # Conditional logic based on role
#         if obj.is_doctor:
#             return {
#                 'doctor_id': staff_metadata.staff_meta_id,
#                 'name': staff_metadata.name,
#                 'speciality': staff_metadata.speciality,
#                 'designation': staff_metadata.designation,
#                 'registration_number': staff_metadata.registration_number,
#                 'consulting_fee': staff_metadata.consulting_fee,
#                 'permanent_address': staff_metadata.permanent_address,
#                 'speciality': staff_metadata.speciality
#             }
#         elif obj.is_nurse:
#             return {
#                 'nurse_id': staff_metadata.staff_meta_id,
#                 'name': staff_metadata.name,
#                 'age': staff_metadata.age,
#                 'gender': staff_metadata.gender,
#                 'permanent_address': staff_metadata.permanent_address,
#                 'designation': staff_metadata.designation,
#             }
#         elif obj.is_pharmacist:
#             return {
#                 'pharmacist_id': staff_metadata.staff_meta_id,
#                 'name': staff_metadata.name,
#                 'registration_number': staff_metadata.registration_number,
#                 'permanent_address': staff_metadata.permanent_address,
#                 'designation': staff_metadata.designation,
#             }
#         elif obj.is_receptionist:
#             return {
#                 'receptionist_id': staff_metadata.staff_meta_id,
#                 'name': staff_metadata.name,
#                 'age': staff_metadata.age,
#                 'gender': staff_metadata.gender,
#                 'permanent_address': staff_metadata.permanent_address,
#                 'designation': staff_metadata.designation,
#             }
#         else:
#             return {}

#     def get_role(self, obj):
#         if obj.is_doctor:
#             return {'is_doctor': True}
#         elif obj.is_nurse:
#             return {'is_nurse': True}
#         elif obj.is_pharmacist:
#             return {'is_pharmacist': True}
#         elif obj.is_receptionist:
#             return {'is_receptionist': True}
#         elif obj.is_admin:
#             return {'is_admin': True}
#         else:
#             return {}

#     def get_clinic_id(self, obj):
#         return obj.clinic_id_id if obj.clinic_id else None  # Use the correct foreign key field name

#     def get_branch_id(self, obj):
#         return obj.branch_id_id if obj.branch_id else None  # Use the correct foreign key field name

class StaffSerializer(serializers.ModelSerializer):
    metadata = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    # clinic_id = serializers.SerializerMethodField()
    # branch_id = serializers.SerializerMethodField()

    class Meta:
        model = Staff_Allotment
        fields = ['staff_id', 'username', 'email', 'mobile_number', 'role', 'metadata']

    def get_metadata(self, obj):
        # Fetch the associated metadata for the staff
        try:
            staff_metadata = Staff_MetaData.objects.get(staff_id=obj.staff_id)
        except Staff_MetaData.DoesNotExist:
            return {}

        # Conditional logic based on role
        metadata = {
            'name': staff_metadata.name,
            'designation': staff_metadata.designation,
            'registration_number': staff_metadata.registration_number,
            'consulting_fee': staff_metadata.consulting_fee,
            'permanent_address': staff_metadata.permanent_address,
        }

        if obj.is_doctor:
            metadata.update({
                'doctor_id': staff_metadata.staff_meta_id,
                'speciality': staff_metadata.speciality,
            })
        elif obj.is_nurse:
            metadata.update({
                'nurse_id': staff_metadata.staff_meta_id,
                'age': staff_metadata.age,
                'gender': staff_metadata.gender,
            })
        elif obj.is_pharmacist:
            metadata.update({
                'pharmacist_id': staff_metadata.staff_meta_id,
            })
        elif obj.is_receptionist:
            metadata.update({
                'receptionist_id': staff_metadata.staff_meta_id,
                'age': staff_metadata.age,
                'gender': staff_metadata.gender,
            })
        return metadata

    def get_role(self, obj):
        if obj.is_doctor:
            return {'is_doctor': True}
        elif obj.is_nurse:
            return {'is_nurse': True}
        elif obj.is_pharmacist:
            return {'is_pharmacist': True}
        elif obj.is_receptionist:
            return {'is_receptionist': True}
        elif obj.is_admin:
            return {'is_admin': True}
        else:
            return {}

    def get_clinic_id(self, obj):
        return obj.clinic_id_id if obj.clinic_id else None  # Use the correct foreign key field name

    def get_branch_id(self, obj):
        return obj.branch_id_id if obj.branch_id else None  # Use the correct foreign key field name




# from rest_framework import serializers
# from app.models import Patient_Registration

class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient_Registration
        fields = ['patient_id', 'patient_name', 'mobile_number', 'email', 'gender', 'address', 'date_of_birth', 'is_registered']
        read_only_fields = ['patient_id']  # patient_id will be auto-generated, so mark it as read-only

    def create(self, validated_data):
        # Generate patient_id in the desired format
        last_patient = Patient_Registration.objects.all().order_by('patient_id').last()
        if last_patient:
            last_code_int = int(last_patient.patient_id[-3:])
            new_patient_id = f"SER{last_code_int + 1:03d}"
        else:
            new_patient_id = "SER001"

        # Assign the generated patient_id
        validated_data['patient_id'] = new_patient_id

        # Create and return the patient instance
        return Patient_Registration.objects.create(**validated_data)
  
    
    
    
    
class PatientAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient_Appointment
        fields = [
            'appointment_id',
            'patient',
            'patient_name',
            'mobile_number',
            'email',
            'doctor',
            'appointment_type',
            'appointment_date',
            'from_time',
            'to_time',
            'notes',
            'is_registered'
        ]

    def to_representation(self, instance):
        """
        Custom representation to show registered and non-registered patients correctly.
        """
        representation = super().to_representation(instance)
        
        # Fetch doctor details
        doctor = instance.doctor
        doctor_name = f"Dr. {doctor.username}"
        speciality = doctor.speciality  # Assuming speciality is stored in the doctor model
        
        # Add custom fields to the output
        representation['doctor_name'] = doctor_name
        representation['speciality'] = speciality
        
        # Ensure patient_id is shown only for registered patients
        if instance.is_registered:
            representation['patient_id'] = instance.patient
        else:
            representation['patient_id'] = None  # Hide patient_id for non-registered patients
            
        return representation
