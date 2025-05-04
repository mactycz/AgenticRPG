import gradio as gr
from interfaces.selection_interface import SelectionInterface
from interfaces.main_interface import MainInterface
from interfaces.character_creation_interface import CharacterCreationInterface
from state import AppState
from styles.css import css

class GradioApp:
    def __init__(self):
        self.app_state = AppState()
        self.selection = SelectionInterface(self.app_state)
        self.main = MainInterface(self.app_state)
        self.character_creation = CharacterCreationInterface(self.app_state)
        self._interfaces = [self.selection, self.main, self.character_creation]

    def launch(self):
        with gr.Blocks(fill_width=True, fill_height=True, css=css) as demo:
            state = gr.State(self.app_state)
            
            with gr.Tabs() as tabs:
                with gr.Tab("API Selection", id="selection_tab"):
                    self.selection.build()
                
                with gr.Tab("Game Interface", id="main_tab", visible=False):
                    self.main.build()
                
                with gr.Tab("Character Creation", id="character_tab", visible=False):
                    self.character_creation.build()
            

            self.selection.register_callbacks()
            self.main.register_callbacks()
            self.character_creation.register_callbacks()
            

            self.selection.components["new_session_btn"].click(
                lambda: gr.Tabs(selected="main_tab"),
                outputs=[tabs]
            )
                        
        demo.launch()

if __name__ == '__main__':
    app = GradioApp()
    app.launch()