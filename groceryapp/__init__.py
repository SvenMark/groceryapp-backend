import firebase_admin
from firebase_admin import credentials
import os

print(os.environ.get('SERVICE_ACCOUNT_KEY'))
print(os.environ)

if os.environ.get('SERVICE_ACCOUNT_KEY') is not None:
    cred = credentials.Certificate(str(os.environ.get("SERVICE_ACCOUNT_KEY")))
else:
    cred = credentials.Certificate("secrets/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
