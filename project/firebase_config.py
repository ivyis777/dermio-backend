import firebase_admin
from firebase_admin import credentials

# Path to your service account file
cred = credentials.Certificate('/home/ubuntu/dermio-backend/project/secure-config/google-servicess.json')
firebase_admin.initialize_app(cred)


