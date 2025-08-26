import gradio as gr
from interfaces.base_interface import BaseInterface
from services.language_model import LanguageModel
from services.image_model import ImageModel
class SelectionInterface(BaseInterface):
    def __init__(self, app_state, navigate_fn=None, tabs_component=None):
        super().__init__(app_state, navigate_fn, tabs_component)

    def build(self):
        self.saved_sessions = self.refresh_sessions()
        with gr.Column() as self.container:
            # LLM Settings Group
            with gr.Group():
                gr.Markdown("<h4 style='text-align: center; margin: 0; padding: 5px;'>LLM Settings</h4>")
                with gr.Row():
                    self.components["api_selection_llm"] = gr.Dropdown(
                        choices=self.app_state.dropdown_options_llm,
                        label="Select API",
                        interactive=True,
                        value="OpenRouter"
                    )
                    self.components["api_auth_llm"] = gr.Dropdown(
                        choices=self.app_state.dropdown_options_api,
                        label="Select auth method",
                        interactive=True,
                        value="Environmental variable token"
                    )
                    self.components["api_key_llm"] = gr.Textbox(
                        label="Enter auth key",
                        interactive=True,
                        value=self.app_state.default_keys["OpenRouter"]
                    )
                
                with gr.Row():
                    self.components["llm_name"] = gr.Dropdown(
                        label="Model name",
                        interactive=True,
                        allow_custom_value=True,
                        value=self.app_state.default_models_llm["OpenRouter"],
                        choices=self.app_state.model_lists["OpenRouter"]
                    )
                    self.components["provider_llm"] = gr.Textbox(
                        label="Provider",
                        interactive=True
                    )
                    self.components["temperature"] = gr.Number(
                        label="Temperature",
                        interactive=True,
                        value=0.7
                    )

            # Image Model Settings Group
            with gr.Group():
                gr.Markdown("<h4 style='text-align: center; margin: 0; padding: 5px;'>Image Model Settings</h4>")
                with gr.Row():
                    self.components["api_selection_image"] = gr.Dropdown(
                        choices=self.app_state.dropdown_options_image,
                        label="Select API",
                        interactive=True,
                        value="Huggingface API"
                    )
                    self.components["api_auth_image"] = gr.Dropdown(
                        choices=self.app_state.dropdown_options_api,
                        label="Select auth method",
                        interactive=True,
                        value="Environmental variable token"
                    )
                    self.components["api_key_image"] = gr.Textbox(
                        label="Enter auth key",
                        interactive=True,
                        value=self.app_state.default_keys["Huggingface API"]
                    )
                
                with gr.Row():
                    self.components["model_name_image"] = gr.Dropdown(
                        label="Image model name",
                        choices=self.app_state.image_models_hf,
                        interactive=True,
                        value=self.app_state.default_models_image["Huggingface API"]
                    )
                    self.components["image_style"] = gr.Textbox(
                        label="Image style",
                        interactive=True
                    )
                    self.components["provider_image"] = gr.Textbox(
                        label="Provider",
                        interactive=True
                    )

            # Session Controls Group
            with gr.Group():
                with gr.Row(equal_height=True):
                    self.components["session_type"] = gr.Dropdown(
                        choices=self.app_state.session_types,
                        interactive=True,
                        value=self.app_state.session_type
                    )
                    self.components["new_session_btn"] = gr.Button(
                        "New session",
                        variant="primary",
                        elem_id="new_session_button"
                    )
                    self.components["saved_sessions"] = gr.Dropdown(
                        label="Saved Sessions",
                        choices=self.saved_sessions,
                        allow_custom_value=False
                    )
                with gr.Row():
                    self.components["load_session_btn"] = gr.Button(
                        "Load Selected Session",
                        interactive=True
                    )

        return self.container
    
    def register_callbacks(self):
        self.session_options=[
            self.components["api_selection_llm"],
            self.components["api_key_llm"],
            self.components["api_auth_llm"],
            self.components["llm_name"],
            self.components["provider_llm"],
            self.components["temperature"],
            self.components["api_selection_image"],
            self.components["api_key_image"],
            self.components["api_auth_image"],
            self.components["model_name_image"],
            self.components["provider_image"],
            self.components["image_style"],
            self.components["session_type"]
        ]
        self.components["load_session_btn"].click(
            fn=self.load_session,
            inputs=[self.components["saved_sessions"]]+self.session_options,
            outputs=[self.tabs_component,self.app_state.interfaces['main'].components["chat_story"].chatbot]
        )
        self.components["new_session_btn"].click(
            fn=self.create_new_session,
            inputs=self.session_options,
            outputs=[self.tabs_component]
        )
    def refresh_sessions(self):
        """Refresh the list of saved sessions"""
        try:
            sessions = self.app_state.session_manager.get_saved_sessions()
            return sessions
        except Exception as e:
            return []
    
    def load_options(self, *args):
        """Load model options and initialize models"""
        if len(args) != 13:
            raise ValueError("Expected 13 arguments for load_options")
            
        (api_llm, api_key_llm, api_auth_llm, llm_name, provider_llm,
        temperature, api_image, api_key_image, api_auth_image,
        model_name_image, provider_image, image_style, session_type) = args
        
        self.app_state.api_selection_llm = api_llm
        self.app_state.api_selection_image = api_image
        self.app_state.session_type = session_type

        self.app_state.llm = LanguageModel(
            api_name=api_llm,
            api_key=api_key_llm,
            api_auth=api_auth_llm,
            model_name=llm_name,
            provider=provider_llm,
            temperature=temperature
        )
        
        self.app_state.image_model = ImageModel(
            api_name=api_image,
            api_key=api_key_image,
            api_auth=api_auth_image,
            model_name=model_name_image,
            provider=provider_image,
            style=image_style
        )

    def create_new_session(self, *args):
        """Create new session using loaded options"""
        try:
            self.load_options(*args)
            
            self.app_state.image_state = {
                "images": [],
                "current_image_index": 0,
                "image_count": 0,
                "current_image_path": None
            }
            if self.app_state.session_type == 'True RPG':
                return self.navigate_fn("character")
            else:
                return self.navigate_fn("main")
            
        except Exception as e:
            gr.Error(f"Failed to create new session: {str(e)}")
            return self.tabs_component

    def load_session(self, session_id,*args):
        """Load session using the same options initialization"""
        if not session_id:
            gr.Error("Please select a session to load")
            return self.tabs_component
        
        try:
            story, session_id, image_state, session_type = self.app_state.session_manager.load_session(session_id)
            self.load_options(*args)
            self.app_state.image_state = image_state
            self.app_state.current_session_id = session_id
            self.app_state.story = story
            self.app_state.session_type = session_type
            gr.Info("Session loaded successfully")
            return self.navigate_fn("main"), story
        
        except Exception as e:
            gr.Error(f"Failed to load session: {str(e)}")
            return self.tabs_component,[]