from flask import Flask, request, send_file
from diffusers import StableDiffusionPipeline
import torch
import io

app = Flask(__name__)

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id)

def generate_dream_image(dream_prompt):
    image = pipe(dream_prompt).images[0]
    return image

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dream_prompt = request.form["dream_prompt"]
        image = generate_dream_image(dream_prompt)
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    return """
    <form method="post">
        <input type="text" name="dream_prompt" placeholder="Enter your dream...">
        <button type="submit">Generate Image</button>
    </form>
    """

if __name__ == "__main__":
    app.run(debug=True)