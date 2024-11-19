import firebase_admin
from firebase_admin import credentials

# Path to your service account file
cred = credentials.Certificate('https://github.com/ivyis777/dermio-backend.git/google-services.json')
firebase_admin.initialize_app(cred)


