import pyrebase

from app.config.env import settings

config = {
    "apiKey": "AIzaSyAQ3au5W0IM2IYutmJfMkiRY8pla1ur1YE",
    "authDomain": "ultesa2022-42cf5.firebaseapp.com",
    "databaseURL": "https://ultesa2022-42cf5.firebaseio.com",
    "projectId": "ultesa2022-42cf5",
    "storageBucket": "ultesa2022-42cf5.appspot.com",
    "messagingSenderId": "988951380167",
    "appId": "1:988951380167:web:b7da784acb4a435bbebee2",
    "measurementId": "G-M4HMTK1PB5"
}

firebase = pyrebase.initialize_app(config)

firebase_storage = firebase.storage()

auth = firebase.auth()
user = auth.sign_in_with_email_and_password(settings.firebase_email, settings.firebase_password)
# before the 1 hour expiry:
user = auth.refresh(user['refreshToken'])
firebase_token = user['idToken']
