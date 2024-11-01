#move all the agentic workflow here and update it to use pipelines instead of agents
from transformers import pipeline
from PIL import Image
from prompts import localPromptStory
from diffusers import DiffusionPipeline

def GenerateText(system_prompt,user_story):
    messages = [
    {"role": "system", "content": system_prompt+user_story},
    ]
    pipe = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.3")
    pipe(messages)
    return messages

def GenerateImage(prompt):
    image.save('RPG.png')
    pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-3.5-large")
    image = pipe(prompt).images[0]
    return image
