import firebase_admin
from firebase_admin import credentials
import os

if os.environ.get('SERVICE_ACCOUNT_KEY'):
    cred = credentials.Certificate(os.environ.get('SERVICE_ACCOUNT_KEY'))
else:
    cred = credentials.Certificate("secrets/serviceAccountKey.json")
firebase_admin.initialize_app(cred)