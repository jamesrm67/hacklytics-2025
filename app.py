import io
from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS

import firebase_admin
from firebase_admin import auth, credentials, db

from nlp import analyze_dream
from image_gen import generate_dream_image
from io import BytesIO
import os
from dotenv import load_dotenv
import base64 #Import base64


# Firebase Service Key Setup
load_dotenv()
cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hacklytics-c838e-default-rtdb.firebaseio.com/'
})

app = Flask(__name__, static_folder="frontend/build", static_url_path="")

app.secret_key = (os.getenv("SECRET_KEY"))

CORS(app, supports_credentials=True)

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
    uid, error_message = verify_firebase_token()
    print(uid, error_message)
    if error_message:
        return jsonify({"error": "Unauthorized", "message": error_message}), 401

    user_id = uid
    dream_text = request.json['dream']
    analysis_dict = analyze_dream(dream_text)

    if isinstance(analysis_dict, dict):  # Check if it's a dictionary
        try:
            interpretation = analysis_dict['interpretation']
            sentiment = analysis_dict['sentiment']
            entities = analysis_dict['entities']
            prompt = generate_image_prompt(interpretation)
                        
            ref = db.reference('dreams')
            new_dream_ref = ref.push()
            new_dream_ref.set({
                'user_id': user_id,
                'dream-text': dream_text,
                'interpretation': interpretation,
                'sentiment': sentiment,
                'entities': entities
            })
            image = generate_dream_image(prompt)
            base64_image = encode_image_to_base64(image)
            
            return jsonify({'analysis': analysis_dict['interpretation']})
        except TypeError as e:
            return jsonify({"analysis error": str(e)}), 700
    else:
        # Handle the string exception case
        print(analysis_dict)
        return jsonify({"error": "Dream analysis failed: " + analysis_dict}), 600

def generate_image_prompt(analysis):
    return f"A dreamlike image, {analysis}, surreal, detailed."

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
 
    try:
        # Store user in Firestore
        user = auth.create_user(email=email, password=password)
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

    if not token:
        return jsonify({"error": "ID token required"}), 400
    
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        return jsonify({"message": "Login successful", "user_id": uid}), 200
    except auth.InvalidIdTokenError as e:
        return jsonify({"error": "Invalid ID token"}), 401
    except Exception as e:
        return jsonify({"error": "Login failed"})

def verify_firebase_token():
    auth_header = request.headers.get('Authorization')
    print(auth_header)
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, "Authorization header missing or invalid"

    id_token = auth_header[len('Bearer '):-1]
    print(id_token)

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return uid, None  # Success, return UID, no error
    except auth.InvalidIdTokenError as e:
        return None, "Invalid Firebase ID token"
    except Exception as e:
        return None, str(e)
    
if __name__ == "__main__":
    app.run(debug=True)