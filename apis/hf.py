#move all the agentic workflow here and update it to use pipelines instead of agents
from transformers import pipeline
from PIL import Image
from diffusers import DiffusionPipeline
from huggingface_hub import InferenceClient

def GenerateText(system_prompt,user_story):
    print(system_prompt+user_story)
    
    client = InferenceClient(
        "mistralai/Mistral-7B-Instruct-v0.3",
    )
    output = client.chat_completion(messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_story + " Story:"},
    ], max_tokens=1000,temperature=0.7).choices[0]["message"]["content"]

    return output

def GenerateImage(prompt):
    client = InferenceClient(
        "stabilityai/stable-diffusion-3.5-large",
    )
    image= client.text_to_image(prompt=prompt)
    image.save('RPG.png')
    return image
