"""
Firebase helper module for the Hospital Multi LLM project.
Provides Firestore initialization and a simple Google user create/get helper.
"""

import os
import json
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

# Local service account JSON file
CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase_key.json')

if not firebase_admin._apps:
    firebase_creds_json = os.getenv('FIREBASE_CREDENTIALS')
    if firebase_creds_json:
        cred_dict = json.loads(firebase_creds_json)
        cred = credentials.Certificate(cred_dict)
    else:
        cred = credentials.Certificate(CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()


def get_or_create_google_user(email, display_name=""):
    """Create or update a user document in Firestore based on Google email."""
    user_id = email.replace('@', '_at_').replace('.', '_dot_')
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()

    if user_doc.exists:
        user_ref.update({'last_login': datetime.utcnow()})
        data = user_doc.to_dict()
        return {
            'user_id': user_id,
            'email': data.get('email', email),
            'display_name': data.get('display_name', display_name or email.split('@')[0])
        }

    user_data = {
        'email': email,
        'display_name': display_name or email.split('@')[0],
        'created_at': datetime.utcnow(),
        'last_login': datetime.utcnow()
    }
    user_ref.set(user_data)
    return {
        'user_id': user_id,
        'email': email,
        'display_name': user_data['display_name']
    }
