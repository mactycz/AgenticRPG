import gradio as gr
from interfaces.base_interface import BaseInterface
from session import get_saved_sessions

class SelectionInterface(BaseInterface):
    def build(self):
        with gr.Column(visible=self.get_visibility()) as self.container:
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
                with gr.Row():
                    self.components["saved_sessions"] = gr.Dropdown(
                        label="Saved Sessions",
                        choices=get_saved_sessions(),
                        allow_custom_value=False
                    )
                with gr.Row():
                    self.components["load_story_btn"] = gr.Button(
                        "Load story",
                        interactive=True
                    )

        return self.container
    

    def register_callbacks(self):
        pass

