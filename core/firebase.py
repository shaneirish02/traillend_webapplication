import firebase_admin
from firebase_admin import credentials
import os
import json

def initialize_firebase():
    if firebase_admin._apps:
        return

    firebase_json = os.environ.get("FIREBASE_KEY_JSON")

    if firebase_json:
        cred_info = json.loads(firebase_json)
        cred = credentials.Certificate(cred_info)
        firebase_admin.initialize_app(cred)
        print("🔥 Firebase initialized from ENV")
    else:
        cred_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "firebase_key.json"
        )
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("🔥 Firebase initialized from local file")
        else:
            raise Exception("❌ Firebase key not found")
