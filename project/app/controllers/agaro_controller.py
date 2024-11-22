from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import time
import json

# Replace with your Agora credentials
APP_ID = "b6940195c7224675aa60a2fe48e2c185"
APP_CERTIFICATE = "e49de8a91c744788a2a70e5d8b248434"

EXPIRATION_TIME_IN_SECONDS = 3600  # Token validity in seconds

def generate_agora_token(request):
    """
    Generates an Agora token for the patient-doctor appointment session.
    """
    try:
        # Extract request data
        data = json.loads(request.body)
        appointment_id = data.get("appointmentId")  # Example: 12345
        user_id = data.get("userId")  # User ID for the patient/doctor

        # Debugging output
        print("Request Data:", data)
        print("Appointment ID:", appointment_id, "User ID:", user_id)

        # Validate request parameters
        if not appointment_id or not user_id:
            return JsonResponse({"error": "appointmentId and userId are required"}, status=400)

        # Define channel name based on appointment ID
        channel_name = f"appointment_{appointment_id}"

        # Calculate token expiration time
        current_time = int(time.time())
        privilege_expired_ts = current_time + EXPIRATION_TIME_IN_SECONDS

        # Generate the RTC token for this user
        token = RtcTokenBuilder.buildTokenWithUid(
            APP_ID,
            APP_CERTIFICATE,
            channel_name,
            int(user_id),  # User ID must be an integer
            1,  # Role_Publisher = 1 (Use 2 for Role_Subscriber)
            privilege_expired_ts
        )

        # Respond with token, channel name, and user ID
        return JsonResponse({
            "token": token,
            "channelName": channel_name,
            "userId": user_id
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format in request body"}, status=400)
    except Exception as e:
        print("Error generating Agora token:", str(e))
        return JsonResponse({"error": "An error occurred while generating the token"}, status=500)
