import os
import firebase_admin
from firebase_admin import credentials, db
import json

firebase_initialized = False

def initialize_firebase():
    global firebase_initialized
    
    if firebase_initialized:
        return
    
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                "private_key_id": "",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDQ\n-----END PRIVATE KEY-----\n",
                "client_email": f"firebase-adminsdk@{os.getenv('FIREBASE_PROJECT_ID', 'default')}.iam.gserviceaccount.com",
                "client_id": "",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"
            })
            
            firebase_admin.initialize_app(cred, {
                'databaseURL': os.getenv('FIREBASE_DATABASE_URL', 'https://default.firebaseio.com')
            })
        
        firebase_initialized = True
        
    except Exception as e:
        print(f"Firebase initialization warning: {str(e)}")
        firebase_initialized = False

def get_bus_location(bus_number):
    """Get live bus location from Firebase"""
    try:
        ref = db.reference(f'buses/{bus_number}')
        data = ref.get()
        
        if data:
            return {
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'timestamp': data.get('timestamp'),
                'speed': data.get('speed', 0)
            }
        return None
    except Exception as e:
        print(f"Error getting bus location: {str(e)}")
        return None

def update_bus_location(bus_number, latitude, longitude, speed=0):
    """Update bus location in Firebase"""
    try:
        ref = db.reference(f'buses/{bus_number}')
        ref.set({
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': db.ServerValue.TIMESTAMP,
            'speed': speed
        })
        return True
    except Exception as e:
        print(f"Error updating bus location: {str(e)}")
        return False

def get_all_bus_locations():
    """Get all bus locations from Firebase"""
    try:
        ref = db.reference('buses')
        data = ref.get()
        return data if data else {}
    except Exception as e:
        print(f"Error getting all bus locations: {str(e)}")
        return {}
