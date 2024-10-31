from loadModel import loadModel
from apis import hf,local,openAI,Anthropic
import gradio as gr
import os
#API key interface - disappears after providing api and shows main interface
def add_key_and_show_interface(api_choice, provided_api_key,provided_api_token):
    global api_key, api_token
    if provided_api_key:
        api_key = provided_api_key
    elif provided_api_token:
        api_token = provided_api_token
    else:
        api_key = ""
    print(api_choice,provided_api_key,provided_api_token)
    connect_to_api(api_choice,provided_api_key,provided_api_token)
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

def connect_to_api(api,api_key="",token_name=""):
    print("Trying connection")
    if api=="Huggingface API":
        if api_key!="":
            print("Provided api key")
            try:
                hf.login(api_key)
            except:
                print("invalid api key")
        elif token_name!="":
            print("Token provided")
            try:
                token = os.environ.get(token_name)
                hf.login(token)
            except:
                print("invalid token or token name")
        elif token=="" and api_key=="":
            print("No auth method provided. This shouldn't be possible")
        LLM = "mistralai/Mistral-7B-Instruct-v0.2"
        ImageModel= "stabilityai/stable-diffusion-xl-base-1.0"
        global clientLLM, clientImage
        clientLLM=hf.hf_load_model(LLM)
        clientImage = hf.hf_load_model(ImageModel)
        print("MODELS LOADED")
    elif api=="local":
        print("local")
