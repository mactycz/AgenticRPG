from loadModel import loadModel
from apis import hf,local,openAI,Anthropic
import gradio as gr
#API key interface - disappears after providing api and shows main interface
def add_key_and_show_interface(api_choice, provided_api_key,provided_api_token):
    global api_key, api_token
    if provided_api_key:
        api_key = provided_api_key
    elif provided_api_token:
        api_token = provided_api_token
    else:
        api_key = ""
    if provided_api_key:
        return gr.update(visible=True),gr.update(visible=False)
    if provided_api_token:
        return gr.update(visible=True),gr.update(visible=False)
    return gr.update(visible=False),gr.update(visible=True)

def update_auth_method(selected_auth):
    if selected_auth == 'API key':
        return gr.update(visible=True), gr.update(visible=False),
    elif selected_auth == 'Enviromental variable token':
        return gr.update(visible=False), gr.update(visible=True)
    else:
        return gr.update(visible=False), gr.update(visible=False)

