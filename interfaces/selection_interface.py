import gradio as gr
from interfaces.base_interface import BaseInterface

class SelectionInterface(BaseInterface):
    def __init__(self, app_state, navigate_fn=None, tabs_component=None):
        super().__init__(app_state, navigate_fn, tabs_component)
    
    def build(self):
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
                    self.components["model_name_image"] = gr.Textbox(
                        label="Image model name",
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

            # Saved Sessions Group
            with gr.Group():
                available_sessions = self.app_state.session_manager.get_saved_sessions()
                gr.Markdown("<h4 style='text-align: center; margin: 0; padding: 5px;'>Saved Sessions</h4>")
                with gr.Row():
                    self.components["saved_sessions"] = gr.Dropdown(
                        label="Saved Sessions",
                        choices=available_sessions,
                        allow_custom_value=False
                    )
                    self.components["refresh_sessions_btn"] = gr.Button("🔄", size="sm")
                
                with gr.Row():
                    self.components["load_session_btn"] = gr.Button(
                        "Load Selected Session",
                        interactive=True
                    )

        return self.container
    
    def register_callbacks(self):
        
        self.components["refresh_sessions_btn"].click(
            fn=lambda: gr.update(choices=self.app_state.session_manager.get_saved_sessions()),
            inputs=[],
            outputs=[self.components["saved_sessions"]]
        )
        

        def load_session_and_navigate(session_id):
            """Load the selected session and navigate to main interface"""
            if not session_id:
                gr.Error("Please select a session to load")
                return self.tabs_component
            
            try:

                _, story, session_id, image_state, session_type = self.app_state.session_manager.load_session(session_id)

                self.app_state.image_state = image_state
                self.app_state.current_session_id = session_id
                self.app_state.session_type = session_type
                self.app_state.story = story 

                gr.Info("Session loaded successfully")
                return self.navigate_fn("main")
            
            except Exception as e:
                gr.Error(f"Failed to load session: {str(e)}")
                return self.tabs_component
        
        self.components["load_session_btn"].click(
            fn=load_session_and_navigate,
            inputs=[self.components["saved_sessions"]],
            outputs=[self.tabs_component]
        )
        

        def update_app_state(api_llm, llm_name, temperature, api_image, image_model, session_type):
            """Update app_state with current interface settings"""
            self.app_state.api_selection_llm = api_llm
            self.app_state.llm_name = llm_name
            self.app_state.temperature = temperature
            self.app_state.api_selection_image = api_image
            self.app_state.model_name_image = image_model
            self.app_state.session_type = session_type
            return None
        

        self.components["new_session_btn"].click(
            fn=update_app_state,
            inputs=[
                self.components["api_selection_llm"],
                self.components["llm_name"],
                self.components["temperature"],
                self.components["api_selection_image"],
                self.components["model_name_image"],
                self.components["session_type"]
            ],
            outputs=None
        ).then(
            fn=lambda: self.navigate_fn("main"),
            outputs=self.tabs_component
        )