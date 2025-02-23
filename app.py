from flask import Flask, request, send_file, render_template, jsonify, session, redirect, url_for, send_from_directory
from flask_cors import CORS

import firebase_admin
from firebase_admin import auth, credentials, db

from nlp import analyze_dream
from image_gen import generate_dream_image
from io import BytesIO
import os
from dotenv import load_dotenv
import base64 #Import base64


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

    if not user_id or not email:
        return jsonify({"error": "Invalid Token"}), 401

    # Store session
    session["user_id"] = user_id
    session["email"] = email

    return jsonify({"message": "Login successful", "user_id": user_id, "email": email}), 200
    
@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out."}), 200

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

@app.route("/test", methods=["POST"])
def test():
    return jsonify({"message": "Test successful"}), 200

if __name__ == "__main__":
    app.run(debug=True)