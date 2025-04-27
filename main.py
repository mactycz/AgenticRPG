import gradio as gr
from interfaces.selection_interface import SelectionInterface
from state import AppState
from styles.css import css
class GradioApp:
    def __init__(self):
        self.app_state = AppState()
        self.selection = SelectionInterface(self.app_state)


    def launch(self):
        with gr.Blocks(fill_width=True, fill_height=True, css=css) as demo:
            self.selection.build()
            self.selection.register_callbacks()
        demo.launch()


if __name__ == '__main__':
    app = GradioApp()
    app.launch()
