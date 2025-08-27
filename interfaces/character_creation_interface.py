import gradio as gr
from interfaces.base_interface import BaseInterface
from prompts import generate_portrait,initialize_story
import os
class CharacterCreationInterface(BaseInterface):
    def __init__(self, app_state, navigate_fn=None, tabs_component=None):
        super().__init__(app_state, navigate_fn, tabs_component)

    def build(self):
        with gr.Column() as self.container:
            with gr.Row():
                with gr.Column(scale=1):
                    self.components["character_description"] = gr.Textbox(label="Character Description",interactive=True,lines=5)
                    self.components["backstory"] = gr.Textbox(label="Backstory",interactive=True,lines = 5)
                    self.components["generate_portrait"] = gr.Button("Generate Portrait")
                with gr.Column(scale=2):
                    self.components["character_portrait"] = gr.Image(height=512,width=512)
                    self.components["character_name"] = gr.Textbox(label="Character Name",interactive=True)
                with gr.Column(scale=1):
                    self.components["str_stat"] = gr.Number(value=10,label="Strength")
                    self.components["dex_stat"] = gr.Number(value=10,label="Dexterity")
                    self.components["con_stat"] = gr.Number(value=10,label="Constitution")
                    self.components["int_stat"] = gr.Number(value=10,label="Intelligence")
                    self.components["wis_stat"] = gr.Number(value=10,label="Wisdom")
                    self.components["cha_stat"] = gr.Number(value=10,label="Charisma")
                    self.components["max_hp"] = gr.Number(value=100,label="Max HP")
            with gr.Row():
                    self.components["begin_adventure"] = gr.Button("Begin Adventure!")
        return self.container
    
    def register_callbacks(self):

        self.components["generate_portrait"].click(
            fn=self.generate_portrait_image,
            inputs = [self.components["character_description"],self.components["backstory"]],
            outputs=self.components["character_portrait"]
        )
        self.components["begin_adventure"].click(
            fn=self.begin_adventure,
            inputs=[
                self.components["character_name"],
                self.components["backstory"],
                self.components["character_description"],
                self.components["character_portrait"]
            ],
            outputs=[self.tabs_component,
                     self.app_state.interfaces['main'].components["chat_story"].chatbot,
                     self.app_state.interfaces['main'].components["true_rpg_interface"],
                     self.app_state.interfaces['main'].components["chat_story"].chatbot
            ]
        )

    def generate_portrait_image(self,description,backstory):
        image_model = self.app_state.image_model
        prompt = self.app_state.llm.generate([{"role": "user", "content": generate_portrait + description + ". Character backstory: "+backstory}])
        if image_model.style != "":
            prompt = prompt + f' Generate the image in {self.app_state.image_model.style} style.'
        image = image_model.generate(prompt)
        image_dir = f"sessions/{self.app_state.session_manager.session_id}/images"
        os.makedirs(image_dir, exist_ok=True)
        image_path = f"{image_dir}/image-{self.components['character_name']}.png"
        image.save(image_path)
        return image_path
    
    def begin_adventure(self,character_name,character_backstory,character_description,character_portrait):
        self.app_state.character_name = character_name
        self.app_state.character_backstory = character_backstory
        self.app_state.character_description = character_description
        self.app_state.character_portrait = character_portrait
        init_story_true_RPG = initialize_story+f"""
        Your character name: {character_name},
        Your backstory: {character_backstory},
        Your description: {character_description}
        """
        self.app_state.story = [(None, init_story_true_RPG)]
        return (
            self.navigate_fn("main"),# tabs
            self.app_state.story,# chatbot history
            gr.update(visible=True),# update visibility
            gr.update(height=384)# update height
        )

        
    