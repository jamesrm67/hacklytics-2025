from flask import Flask, request, send_file, render_template, jsonify, session, redirect, url_for
from flask_cors import CORS

import firebase_admin
from firebase_admin import auth, credentials, db

from nlp import analyze_dream
from image_gen import generate_dream_image
import io
import os
from dotenv import load_dotenv

load_dotenv()
cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hacklytics-c838e-default-rtdb.firebaseio.com/'
})

app = Flask(__name__)

app.secret_key = (os.getenv("SECRET_KEY"))

CORS(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dream_text = request.form["dream_text"]      
        analysis = analyze_dream(dream_text)
        interpretation = analysis.get("interpretation", "No interpretation available.")
        
        return render_template("index.html", interpretation=interpretation)
    else:
        return render_template("index.html")

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
    print("Registering user...")
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
        uid = decoded_token["uid"]
        email = decoded_token["email"]
        
        if not uid or not email:
            return None, None
        return uid, email, ""
    except auth.InvalidIdTokenError as e:
        print(f"Token verification failed: {e}")
        return None, None
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