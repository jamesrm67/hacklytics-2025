from flask import Flask, request, send_file, render_template
from nlp import analyze_dream
from image_gen import generate_dream_image
import io

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
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

@app.route("/analyze", methods=["POST"])
def analyze():
    dream_text = request.form.get["dream_text"]
    if not dream_text:
        return "No dream text provided", 400
    analysis = analyze_dream(dream_text)
    return analysis

if __name__ == "__main__":
    app.run(debug=True)