import gradio as gr
from interfaces.base_interface import BaseInterface
from session import get_saved_sessions
from app import chat
class MainInterface(BaseInterface):
    def __init__(self, app_state):
        super().__init__(app_state)
        self._visible = False

    def build(self):
        with gr.Column(visible=self.visible) as self.container:

            with gr.Row():
                with gr.Column():
                    chat_story = gr.ChatInterface(
                    fn=chat,
                    chatbot=gr.Chatbot(height=self.app_state.chat_height.value,
                        value=[(None,self.app_state.initialize_story_state.value)]),
                        additional_inputs=[self.app_state.character_backstory,self.app_state.api_selection_llm,self.app_state.llm_name,self.app_state.temperature,self.app_state.session_type,
                            gr.Checkbox(label ="Automatically generate an image")])
                    
                    with gr.Row(visible=False, elem_classes="character-card") as True_RPG_interface:
                        with gr.Column(min_width=300, elem_classes="identity-column"):
                            character_portrait_main =  gr.Image("helpers/placeholder.png", 
                                    elem_classes="character-portrait",
                                    interactive=False,
                                    min_width=300)
                        with gr.Column(elem_classes="stats-column"):                        
                            with gr.Column(elem_classes="stats-grid"):
                                str_main=gr.Markdown("🗡 **Strength**: 18", elem_classes="stat-item")
                                dex_main=gr.Markdown("🏹 **Dexterity**: 14", elem_classes="stat-item")
                                int_main=gr.Markdown("📚 **Intelligence**: 16", elem_classes="stat-item")
                                wis_main=gr.Markdown("🔮 **Wisdom**: 12", elem_classes="stat-item")
                                con_main=gr.Markdown("❤️ **Constitution**: 15", elem_classes="stat-item")
                                cha_main=gr.Markdown("🎭 **Charisma**: 10", elem_classes="stat-item")
                            with gr.Column(elem_classes="name-container"):
                                character_name_main=gr.Markdown("**Character Name**", 
                                        elem_classes="name-text")
                                hp_main=gr.Markdown("**❤ 100/100**", 
                                        elem_classes="health-text")
                                with gr.Row(elem_classes="result-container"):
                                    roll_button = gr.Button("🎲", elem_id="dice-button", elem_classes="dice-button")
                                    roll_results = gr.Markdown("", elem_id="dice-result", elem_classes="dice-result")

                with gr.Column():
                    change_api = gr.Button("Change API")
                    image= gr.Image(self.app_state.image_state.value["current_image_path"],label="Image",height=512,type='filepath')
                    with gr.Row():
                        previous = gr.Button("←")
                        counter = gr.Button(f"{self.app_state.image_state.value['current_image_index']}/{self.app_state.image_state.value['image_count']}")
                        next = gr.Button("→")
                    image_button = gr.Button("Generate Image")

    
                    with gr.Row():
                        save_name = gr.Textbox(label="Story name",interactive=True,value="")
                        save_option = gr.Dropdown(label="Save option",choices=["Full session","Session summary"],interactive=True)
                        save_story_button = gr.Button("Save the story")
        return self.container