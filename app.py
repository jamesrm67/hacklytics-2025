import base64
from flask import Flask, request, send_file, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user, login_user, logout_user

import firebase_admin
from firebase_admin import auth, credentials, db

from nlp import analyze_dream
from image_gen import generate_dream_image
import io
import os
from dotenv import load_dotenv

from models.User import User

# Firebase Service Key Setup
load_dotenv()
cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hacklytics-c838e-default-rtdb.firebaseio.com/'
})

app = Flask(__name__)

app.secret_key = (os.getenv("SECRET_KEY"))

CORS(app)

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)

# User loader function
@login_manager.user_loader
def load_user(user_id):
    # Fetch user data from Firebase Realtime Database using user_id
    ref = db.reference(f'users/{user_id}')
    user_data = ref.get()
    if user_data:
        user = User(id=user_id, **user_data)
        return user
    return None

@app.route("/interpret", methods=['POST'])
# @login_required
def interpret():
    dream_text = request.get_json()
    if not dream_text:
        return jsonify({'error': 'No dream text provided'}), 400
    
    try:
        analysis = analyze_dream(dream_text)
        if not analysis:
            return jsonify({"error": "No analysis."})
        entities = analysis.get('entities')
        sentiment = analysis.get('sentiment')
        interpretation = analysis.get('interpretation')
        
        img_prompt = generate_image_prompt(interpretation)
        image = generate_dream_image(img_prompt)
        base64_img = encode_image_to_base64(image)
        
        # ref = db.reference('dreams')
        # new_dream_ref = ref.push()
        # new_dream_ref.set({
        #     'user_id': current_user.id,
        #     'dream-text': dream_text,
        #     'interpretation': interpretation,
        #     'sentiment': sentiment,
        #     'entities': entities
        # })
        
        response_data = {
            'Entities': entities,
            'Sentiment': sentiment,
            'Interpretation': interpretation,
            'Img': base64_img
        }
        
        return jsonify(response_data)
    except AttributeError:
        return jsonify({"error": "Attribute Error"}), 401
    except auth.RevokedIdTokenError:
        return jsonify({"error": "Token revoked"}), 401
    except auth.InvalidIdTokenError:
        return jsonify({"error": "Invalid token id"}), 401

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    user = auth.create_user(email=email, password=password)
    
    try:
        # Store user in Firestore
        user_ref = db.reference('/users/' + user.uid)
        user_ref.set({
            'name': name,
            "email": email
        })
        return jsonify({"message": "User registered successfully"}), 200
    except Exception as e:
        print(f"Error registering user: {e}")
        return jsonify({"error": "Failed to register user"}), 500
    
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    token = data
    user_id, email, error_message = verify_token(token)

    ref = db.reference(f'users/{user_id}')
    user_data = ref.get()

    if user_data:
        user = User(id=user_id, username=user_data.get('name'), email=email)
        login_user(user)
        return jsonify({"message": "Login successful", "user_id": user_id, "email": email}), 200
    else:
        return jsonify({"error": "User not found"}), 404
    
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Successfully logged out."})

def verify_token(user_token):
    try:
        decoded_token = auth.verify_id_token(user_token)
        uid = decoded_token["uid"]
        email = decoded_token["email"]
        
        if not uid or not email:
            return None, None
        
        return uid, email, ""
    except auth.InvalidIdTokenError as e:
        print(f"Token verification failed: {e}")
        return jsonify({"error": "Invalid Id Token"})
    except Exception as e:
        return str(e)
    
def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def generate_image_prompt(analysis):
    return f"A dreamlike image, {analysis}, surreal, detailed."

if __name__ == "__main__":
    app.run(debug=True)