from prompts import initialize_story
from session import SessionManager
class AppState:
    def __init__(self):
        self.session_manager = SessionManager()
        
        self.current_session_id = None
        self.current_session_name = None
        self.image_state = {
            "current_image_path": "helpers/placeholder.png",
            "current_image_index": 0,
            "image_count": 0
        }
        self.dropdown_options_llm = ['Local','Huggingface API','OpenAI','Anthropic','OpenRouter']
        self.dropdown_options_image = ['Local','Huggingface API','OpenAI']
        self.dropdown_options_api = ['','API key', 'Environmental variable token']
        self.default_keys = {
            'Local':'',
            'Huggingface API':'HF_API_KEY',
            'OpenAI':'OPENAI_API_KEY',
            'Anthropic':'ANTHROPIC_API_KEY',
            'OpenRouter':'OPENROUTER_API_KEY'
        }
        self.models_openai=["gpt-4o","chatgpt-4o-latest","gpt-4o-mini","o1","o1-mini","o3-mini","o1-preview"]
        self.models_anthropic=["claude-3-5-sonnet-latest","claude-3-5-haiku-latest","claude-3-opus-latest","claude-3-sonnet-20240229","claude-3-haiku-20240307"]
        self.models_hf=[]
        self.model_lists = {
            'Local':'',
            'Huggingface API':self.models_hf,
            'OpenAI':self.models_openai,
            'Anthropic':self.models_anthropic,
            'OpenRouter': self.models_hf
        }
        self.default_models_llm = {
            'Local':'',
            'Huggingface API':'meta-llama/Llama-3.1-8B-Instruct',
            'OpenAI':'gpt-4o',
            'Anthropic':'claude-3-5-sonnet-latest',
            'OpenRouter':'x-ai/grok-3-mini-beta'
        }
        self.default_models_image = {
            'Local':'',
            'Huggingface API':'stabilityai/stable-diffusion-3.5-large-turbo',
            'OpenAI':'dall-e-3'
        }
        self.api_key = ""
        self.api_token = ""
        self.session_types =["ABCD options","Text adventure","True RPG"]
        self.chat_height={"ABCD options":512,"Text adventure":512,"True RPG":400}
        self.true_rpg_interface = {"ABCD options":False,"Text adventure":False,"True RPG":True}
        self.roll_needed = False
        self.session_type = "ABCD options"
        self.chat_height={"ABCD options":512,"Text adventure":512,"True RPG":400}
        self.initialize_story = initialize_story
        self.character_backstory = ""
        self.api_selection_llm = "Huggingface API"
        self.api_selection_image = "Huggingface API"
        self.llm_name = "meta-llama/Llama-3.1-8B-Instruct"
        self.temperature = 0.7
        self.character_name = ""
        self.character_description = ""
        self.character_portrait = "helpers/placeholder.png"
        self.auto_generate_image=False
        self.story=""
        self.text_returned=False