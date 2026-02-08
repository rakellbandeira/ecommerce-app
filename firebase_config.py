import firebase_admin
from firebase_admin import credentials, firestore

# service account key
cred = credentials.Certificate('config/serviceAccountKey.json')

try:
    firebase_admin.get_app()
except ValueError:
    # initialize it
    firebase_admin.initialize_app(cred)

# Get Firestore database
db = firestore.client()