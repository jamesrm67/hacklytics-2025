import io
from flask import Flask, request, send_file, render_template, jsonify, session, redirect, url_for, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user, login_user, logout_user

import firebase_admin
from firebase_admin import auth, credentials, db

from nlp import analyze_dream
from image_gen import generate_dream_image
from io import BytesIO
import os
from dotenv import load_dotenv
import base64 #Import base64

from models.User import User

# Firebase Service Key Setup
load_dotenv()
cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hacklytics-c838e-default-rtdb.firebaseio.com/'
})

app = Flask(__name__, static_folder="frontend/build", static_url_path="")

app.secret_key = (os.getenv("SECRET_KEY"))

CORS(app)


def encode_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

@app.route('/')
def index():
    return send_from_directory(app.static_folder,'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/analyze', methods=['POST'])
def analyzer():
    dream_text = request.json['dream']
    analysis_dict = analyze_dream(dream_text)

    if isinstance(analysis_dict, dict):  # Check if it's a dictionary
        try:
            prompt = generate_image_prompt(analysis_dict['interpretation'])
            image = generate_dream_image(prompt)
            base64_image = encode_image_to_base64(image)
            return jsonify({'analysis': analysis_dict['interpretation'], 'image_data': base64_image})
        except TypeError as e:
            return jsonify({"error": str(e)}), 500
    else:
        # Handle the string exception case
        return jsonify({"error": "Dream analysis failed: " + analysis_dict}), 500

def generate_image_prompt(analysis):
    return f"A dreamlike image, {analysis}, surreal, detailed."
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
        entities = analysis.get('entities')
        sentiment = analysis.get('sentiment')
        interpretation = analysis.get('interpretation')
        
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
            'Interpretation': interpretation
        }
        
        return jsonify(response_data)
    except auth.RevokedIdTokenError:
        return jsonify({"error": "Token revoked"}), 401
    except auth.InvalidIdTokenError:
        return jsonify({"error": "Invalid token id"}), 401

@app.route("/generate_img", methods=["POST"])
def generate_img():
    if request.method == "POST":
        dream_prompt = request.form["dream_prompt"]
        image = generate_dream_image(dream_prompt)
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

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
    
@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"message": f"Welcome, {session['email']}!"}), 200

if __name__ == "__main__":
    app.run(debug=True)