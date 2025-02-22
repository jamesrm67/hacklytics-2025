from flask import Flask, request, send_file, render_template, jsonify, session, redirect, url_for
from flask_cors import CORS

import firebase_admin
from firebase_admin import credentials, firestore, auth

from nlp import analyze_dream
from image_gen import generate_dream_image
from io import BytesIO
import os
from dotenv import load_dotenv
import base64 #Import base64


app = Flask(__name__)
CORS(app, support_credentials=True)

load_dotenv()
app.secret_key = (os.getenv("SECRET_KEY"))

cred = credentials.Certificate("hacklytics25servicekey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


app = Flask(__name__)


def encode_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route("/register", methods=["POST"])
def register():
    token = request.json.get("token")
    user_id, email = verify_token(token)

    if not user_id:
        return jsonify({"error": "Invalid Token"}), 401

    # Store user in Firestore
    user_ref = db.collection("users").document(user_id)
    user_ref.set({"email": email}, merge=True)

    return jsonify({"message": "User registered successfully"}), 200

@app.route("/login", methods=["POST"])
def login():
    token = request.json.get("token")
    user_id, email = verify_token(token)

    if not user_id:
        return jsonify({"error": "Invalid Token"}), 401

    # Store session
    session["user_id"] = user_id
    session["email"] = email

    return jsonify({"message": "Login successful", "user_id": user_id, "email": email}), 200
    
@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("index"))

def verify_token(user_token):
    try:
        decoded_token = auth.verify_id_token(user_token)
        return decoded_token["uid"], decoded_token["email"]
    except Exception as e:
        return str(e)
    
@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"message": f"Welcome, {session['email']}!"}), 200


if __name__ == '__main__':
    app.run(debug=True)
