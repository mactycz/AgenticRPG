import gradio as gr
from interfaces.base_interface import BaseInterface

class CharacterCreationInterface(BaseInterface):
    def __init__(self, app_state, navigate_fn=None, tabs_component=None):
        super().__init__(app_state, navigate_fn, tabs_component)

    def build(self):
        with gr.Column() as self.container:
            with gr.Row():
                with gr.Column(scale=1):
                    self.character_description = gr.Textbox(label="Character Description",interactive=True,lines=5)
                    self.backstory = gr.Textbox(label="Backstory",interactive=True,lines = 5)
                    self.generate_portrait = gr.Button("Generate Portrait")
                with gr.Column(scale=2):
                    self.character_portrait = gr.Image(height=512,width=512)
                    self.character_name = gr.Textbox(label="Character Name",interactive=True)
                with gr.Column(scale=1):
                    self.str_stat = gr.Number(value=10,label="Strength")
                    self.dex_stat = gr.Number(value=10,label="Dexterity")
                    self.con_stat = gr.Number(value=10,label="Constitution")
                    self.int_stat = gr.Number(value=10,label="Intelligence")
                    self.wis_stat = gr.Number(value=10,label="Wisdom")
                    self.cha_stat = gr.Number(value=10,label="Charisma")
                    self.max_hp = gr.Number(value=100,label="Max HP")
            with gr.Row():
                    self.begin_adventure = gr.Button("Begin Adventure!")
        return self.container
    def register_callbacks(self):
        pass
    