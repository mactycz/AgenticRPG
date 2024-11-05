from loadModel import loadModel
from apis import hf,local,openAI,Anthropic
import gradio as gr
import os
#API key interface - disappears after providing api and shows main interface
clientLLM, clientImage = None, None
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

def update_placeholders(option,auth,keys):
    if auth=="Enviromental variable token":
        return gr.update(value=keys[option])

def connect_to_api(api,auth,key):
    print("Trying connection")
    if key=="":
        print("No key provided")
    if api=="Huggingface API":
        if auth=="API key":
            print("Provided api key")
            try:
                hf.login(api_key)
            except:
                print("invalid api key")
        elif auth=="Enviromental variable token":
            print("Token provided: "+key)
            try:
                token = os.environ.get(key)
                print("Token: "+token)
                hf.login(token)
            except:
                print("invalid token or token name")
        elif token=="" and api_key=="":
            print("No auth method provided. This shouldn't be possible")
        print("MODELS LOADED")
    elif api=="local":
        print("local")


