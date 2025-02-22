import base64

from flask import Flask, request, send_file, render_template
from nlp import analyze_dream
from image_gen import generate_dream_image
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dream_text = request.form["dream_text"]
        if not dream_text:
            return "No dream text provided", 400
        
        analysis = analyze_dream(dream_text)
        interpretation = analysis["interpretation"]

        dream_prompt = interpretation

        image = generate_dream_image(dream_prompt)

        if image:
            img_io = io.BytesIO()
            image.save(img_io, 'PNG')
            img_io.seek(0)
            img_data = f"data:image/png;base64,{base64.b64encode(img_io.read()).decode('utf-8')}"
        else:
            img_data = None
        
        return render_template("index.html", interpretation=interpretation, img_data=img_data)
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

@app.route("/analyze", methods=["POST"])
def analyze():
   dream_text = request.form.get("dream_text")
   if not dream_text:
       return jsonify({"error" : "No dream text provided"}), 400

   analysis = analyze_dream(dream_text)

   image_prompt = f"A dream with {', '.join(analysis['entities'])}. The sentiment is {analysis['sentiment']}"

   image = generate_dream_image(image_prompt)

   img_io = io.BytesIO()
   image.save(img_io, 'PNG')
   img_io.seek(0)
   image_data = base64.b64encode(img_io.getvalue()).decode('utf-8')

   return jsonify({
       "analysis": analysis,
       "image_data": image_data
   })


if __name__ == "__main__":
    app.run(debug=True)