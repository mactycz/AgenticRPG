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

    def toggle_interfaces(self, interface_to_show):
        updates = []
        for interface in self._interfaces:
            visible = interface == interface_to_show
            updates.append(gr.update(visible=visible))
        return updates
        

    def launch(self):
        with gr.Blocks(fill_width=True, fill_height=True, css=css) as demo:
            self.selection.build()
            self.selection.register_callbacks()
            self.main.build()
            self.character_creation.build()

            self.selection.components["new_session_btn"].click(
                lambda: self.toggle_interfaces(self.main),
                outputs=[self.selection.container, self.main.container, self.character_creation.container]  
            )
        
        
        demo.launch()


if __name__ == '__main__':
    app = GradioApp()
    app.launch()
