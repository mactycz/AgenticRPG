import gradio as gr
from interfaces.base_interface import BaseInterface
from app import chat

class MainInterface(BaseInterface):
    def __init__(self, app_state, navigate_fn=None, tabs_component=None):
        super().__init__(app_state, navigate_fn, tabs_component)

    def build(self):
        with gr.Column() as self.container:
            with gr.Row():
                with gr.Column():
                    # Chat interface
                    self.components["chat_story"] = gr.ChatInterface(
                        fn=chat,
                        chatbot=gr.Chatbot(
                            height=512,
                            value=[(None, self.app_state.initialize_story)]
                        ),
                        # additional_inputs=[
                        #     self.app_state.character_backstory,
                        #     self.app_state.api_selection_llm,
                        #     self.app_state.llm_name,
                        #     self.app_state.temperature,
                        #     self.app_state.session_type,
                        #     gr.Checkbox(label="Automatically generate an image")
                        # ]
                    )
                    
                    # # RPG interface
                    # self.components["true_rpg_interface"] = gr.Row(visible=False)
                    # with self.components["true_rpg_interface"]:
                    #     with gr.Column(min_width=300):
                    #         self.components["character_portrait_main"] = gr.Image(
                    #             "helpers/placeholder.png", 
                    #             interactive=False,
                    #             min_width=300
                    #         )
                    #     with gr.Column():
                    #         with gr.Column():
                    #             self.components["str_main"] = gr.Markdown("🗡 **Strength**: 18")
                    #             self.components["dex_main"] = gr.Markdown("🏹 **Dexterity**: 14")
                    #             self.components["int_main"] = gr.Markdown("📚 **Intelligence**: 16")
                    #             self.components["wis_main"] = gr.Markdown("🔮 **Wisdom**: 12")
                    #             self.components["con_main"] = gr.Markdown("❤️ **Constitution**: 15")
                    #             self.components["cha_main"] = gr.Markdown("🎭 **Charisma**: 10")
                    #         with gr.Column():
                    #             self.components["character_name_main"] = gr.Markdown("**Character Name**")
                    #             self.components["hp_main"] = gr.Markdown("**❤ 100/100**")
                    #             with gr.Row():
                    #                 self.components["roll_button"] = gr.Button("🎲")
                    #                 self.components["roll_results"] = gr.Markdown()

                with gr.Column():
                    # Right column components
                    self.components["change_api"] = gr.Button("Change API")
                    self.components["image"] = gr.Image(
                        self.app_state.image_state["current_image_path"],
                        label="Image",
                        height=512,
                        type='filepath'
                    )
                    with gr.Row():
                        self.components["previous"] = gr.Button("←")
                        self.components["counter"] = gr.Button(
                            f"{self.app_state.image_state['current_image_index']}/"
                            f"{self.app_state.image_state['image_count']}"
                        )
                        self.components["next"] = gr.Button("→")
                    self.components["image_button"] = gr.Button("Generate Image")
    
                    with gr.Row():
                        self.components["save_name"] = gr.Textbox(
                            label="Story name",
                            interactive=True,
                            value=""
                        )
                        self.components["save_option"] = gr.Dropdown(
                            label="Save option",
                            choices=["Full session","Session summary"],
                            interactive=True
                        )
                        self.components["save_story_button"] = gr.Button("Save the story")
        
        return self.container
    
    def register_callbacks(self):
        pass