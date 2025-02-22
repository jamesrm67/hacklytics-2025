from flask import Flask, request, send_file, render_template, jsonify, session, redirect, url_for
from flask_cors import CORS

import firebase_admin
from firebase_admin import credentials, firestore, auth

from nlp import analyze_dream
from image_gen import generate_dream_image
import io

app = Flask(__name__)
CORS(app, support_credentials=True)
app.secret_key = "supersecretkey"

cred = credentials.Certificate("hacklytics25servicekey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dream_text = request.form["dream_text"]
        if not dream_text:
            return "No dream text provided", 400
        
        analysis = analyze_dream(dream_text)
        interpretation = analysis["interpretation"]
        
        return render_template("index.html", interpretation=interpretation)
    else:
        return render_template("index.html")

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

@app.route("/generate_img", methods=["POST"])
def generate_img():
    if request.method == "POST":
        dream_prompt = request.form["dream_prompt"]
        image = generate_dream_image(dream_prompt)
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)