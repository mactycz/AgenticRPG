import requests
from io import BytesIO
from PIL import Image
from openai import OpenAI
from huggingface_hub import InferenceClient
from .base_model import BaseModel
import os
class ImageModel(BaseModel):
    def __init__(self, api_name, api_key,api_auth, model_name, provider="", style=""):
        super().__init__(api_name, api_key,api_auth, model_name, provider)
        self.style = style
        self.timeout=30
        self.connect()
        
    def connect(self):
        """Connect to the selected API"""
        if self.api_auth == "Environmental variable token":
            self.api_key = os.environ.get(self.api_key)
        if self.api_name == "Huggingface API":
            provider = self.provider if self.provider != "" else "hf-inference"
            self.client = InferenceClient(
                provider=provider,
                api_key=self.api_key
            )
            
        elif self.api_name == "OpenAI":
            self.client = OpenAI(api_key=self.api_key)
            
        elif self.api_name == "Local":
            print("Local image generation not implemented")
            self.client = None
            
        else:
            raise ValueError(f"Unsupported API: {self.api_name}")
    
    def set_style(self, style):
        """Set the image generation style"""
        self.style = style
        
    def generate(self,prompt):
        api_call = {
            "OpenAI" : lambda prompt: self.client.images.generate(prompt=prompt,model=self.model_name,timeout=30),
            "Huggingface API" : lambda prompt : self.client.text_to_image(prompt=prompt,model=self.model_name),
            "Deepinfra": lambda prompt: self.client.images.generate(prompt=prompt,model=self.model_name,timeout=30),
        }
        image = api_call[self.api_name](prompt)
        if self.api_name == "OpenAI":
            image_url = image.data[0].url
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                return Image.open(BytesIO(image_response.content))
            else:
                raise Exception("Failed to download OpenAI image")

        return image