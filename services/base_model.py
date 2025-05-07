# models/base_model.py
from abc import ABC, abstractmethod

class BaseModel(ABC):
    def __init__(self, api_name, api_key,api_auth, model_name, provider=""):
        self.api_name = api_name
        self.api_key = api_key
        self.api_auth = api_auth
        self.model_name = model_name
        self.provider = provider
        self.client = None
        
    @abstractmethod
    def connect(self):
        """Establish connection to the API"""
        pass
        
    @abstractmethod
    def generate(self, *args, **kwargs):
        """Generate content using the model"""
        pass