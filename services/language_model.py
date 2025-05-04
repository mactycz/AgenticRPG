# models/llm.py
import anthropic
from openai import OpenAI
from .base_model import BaseModel
from local import LocalLlamaClient, LocalTransformersClient

class LanguageModel(BaseModel):
    def __init__(self, api_name, api_key, model_name, provider="", temperature=0.7, max_tokens=2000,system_message=""):
        super().__init__(api_name, api_key, model_name, provider)
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_message = system_message
        self.connect()
        
    def connect(self):
        """Connect to the selected API"""
        if self.api_name == "Huggingface API":
            if self.provider == "" or self.provider == "HF Inference API":
                base_url = "https://router.huggingface.co/hf-inference/v1"
            else:
                base_url = f"https://router.huggingface.co/{self.provider}"
            self.client = OpenAI(base_url=base_url, api_key=self.api_key)
            
        elif self.api_name == "OpenAI":
            self.client = OpenAI(api_key=self.api_key)
            
        elif self.api_name == "Anthropic":
            self.client = anthropic.Anthropic(api_key=self.api_key)
            
        elif self.api_name == "Local":
            try:
                if "gguf" in self.model_name:
                    self.client = LocalLlamaClient(self.model_name)
                else:
                    self.client = LocalTransformersClient(self.model_name)
                print(f"Local model loaded: {self.model_name}")
            except Exception as e:
                print(f"Error loading local model: {str(e)}")
                
        elif self.api_name == "OpenRouter":
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key
            )
        else:
            raise ValueError(f"Unsupported API: {self.api_name}")
            
    def generate(self, messages, temperature=None, max_tokens=None):
        """Generate text based on the provided messages"""
        # Use instance params if not provided in call
        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        api_call={
        "Huggingface API": lambda msgs:self.client.chat.completions.create(messages=msgs,model = self.model_name,temperature=temperature,max_tokens=max_tokens).choices[0].message.content,
        "OpenAI": lambda msgs: self.client.chat.completions.create(model=self.model_name,messages=msgs, temperature=temperature, max_tokens=max_tokens).choices[0].message.content,
        "Anthropic": lambda msgs: self.client.messages.create(model=self.model_name,messages=msgs, temperature=temperature, max_tokens=max_tokens,system=self.system_message).content[0].text,
        "OpenRouter":lambda msgs: self.client.chat.completions.create(messages=msgs,model = self.model_name,temperature=temperature,max_tokens=max_tokens).choices[0].message.content,
        "Local": lambda msgs: self.client.generate_response(msgs)
        }
        return api_call[self.api_name](messages)