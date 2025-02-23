from diffusers import StableDiffusionPipeline

model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id)

def generate_dream_image(dream_prompt):
    image = pipe(dream_prompt).images[0]
    return image

