import gradio as gr
from interfaces.selection_interface import SelectionInterface
from interfaces.main_interface import MainInterface
from interfaces.character_creation_interface import CharacterCreationInterface
from state import AppState
from styles.css import css

class GradioApp:
    def __init__(self):
        self.app_state = AppState()
        self.tabs = None 
        self.interfaces = {}

    def navigate_to(self, tab_name):
        """Global navigation function"""
        print(f"Navigating to {tab_name}")
        tab_index = list(self.interfaces.keys()).index(tab_name)
        return gr.Tabs(selected=tab_index)
    def launch(self):
        with gr.Blocks(fill_width=True, fill_height=True, css=css) as demo:
            with gr.Tabs() as tabs:
                self.tabs = tabs
                
                self.interfaces = {
                    "selection": SelectionInterface(self.app_state, self.navigate_to, self.tabs),
                    "main": MainInterface(self.app_state, self.navigate_to, self.tabs),
                    "character": CharacterCreationInterface(self.app_state, self.navigate_to, self.tabs)
                }
                
                tab_items = []
                for i, (name, interface) in enumerate(self.interfaces.items()):
                    with gr.TabItem(label=name.capitalize(), id=i) as tab:
                        interface.build()
                        tab_items.append(tab)
            
            for interface in self.interfaces.values():
                interface.register_callbacks()
            
        demo.launch()
if __name__ == '__main__':
    app = GradioApp()
    app.launch()