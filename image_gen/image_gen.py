from diffusers import StableDiffusionPipeline

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id)

def generate_dream_image(dream_prompt):
    image = pipe(dream_prompt).images[0]
    return image