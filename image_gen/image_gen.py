from diffusers import StableDiffusionPipeline

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id)

def generate_dream_image(dream_prompt):
    try:
        image = pipe(dream_prompt).images[0]
        return image
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

