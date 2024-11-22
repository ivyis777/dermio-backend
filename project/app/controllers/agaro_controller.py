from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import time,json


# Replace with your Agora App ID and App Certificate
APP_ID = "b6940195c7224675aa60a2fe48e2c185"
APP_CERTIFICATE = "e49de8a91c744788a2a70e5d8b248434"
EXPIRATION_TIME_IN_SECONDS = 36000  # Token validity (e.g., 10 hour)

def generate_agora_token(request):
    """
    Generates an Agora token for the patient-doctor appointment session.
    """
    # Extract appointment details
    data = json.loads(request.body)
    print("data :",data)


    appointment_id = request.data.get("appointmentId")  # Example: 12345
    user_id = request.data.get("userId")  # User ID for the patient/doctor

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
        RtcTokenBuilder.Role_Attendee,
        privilege_expired_ts
    )

    # Respond with token, channel name, and user ID
    return JsonResponse({
        "token": token,
        "channelName": channel_name,
        "userId": user_id
    })
