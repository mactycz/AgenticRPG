from loadModel import loadModel
import gradio as gr
import os
#API key interface - disappears after providing api and shows main interface
from prompts import *
from PIL import Image
from diffusers import DiffusionPipeline
clientLLM = None
clientImage = None
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
        from huggingface_hub import login

        if auth=="API key":
            print("Provided api key")
            try:
                login(api_key)
            except:
                print("invalid api key")
        elif auth=="Enviromental variable token":
            print("Token provided: "+key)
            try:
                token = os.environ.get(key)
                print("Token: "+token)
                login(token)
            except:
                print("invalid token or token name")
        elif token=="" and api_key=="":
            print("No auth method provided. This shouldn't be possible")
        global clientLLM
        clientLLM=Client()
        global clientImage
        clientImage=Client("stabilityai/stable-diffusion-3.5-large")
        print(clientLLM)
        print("MODELS LOADED")
    elif api=="local":
        print("local")
def Client(model="Qwen/Qwen2.5-72B-Instruct"):
    from huggingface_hub import InferenceClient
    global client 
    client= InferenceClient(
        "Qwen/Qwen2.5-72B-Instruct"
    )
    return client

def Chat(message,history,abcd=False):
    messages=[]
    messages.append({"role": "system", "content": localPromptStory})
    if len(history) == 1:
        messages.append({"role": "assistant", "content": initialize_story})
        messages.append({"role": "user", "content": localPromptStory+message})
        output = clientLLM.chat_completion(messages, max_tokens=1000,temperature=0.7).choices[0]["message"]["content"]
        history.append([None,localPromptStory+message])
        history.append([localPromptStory+message,output])
    else:
        for user_msg, bot_msg in history:
            if user_msg is not None:
                messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
        messages.append({"role": "user", "content": message})
        print(messages)
        response = clientLLM.chat_completion(messages, max_tokens=50,temperature=0.7)
        output = response.choices[0]["message"]["content"]
        history.append((message,output))
    return output
    #     output = clientLLM.chat_completion(messages = 
    #         history, max_tokens=10,temperature=0.7).choices[0]["message"]["content"]
    #     print(output)
    #     history.append({"role": "system", "content": output})
    # print(history)
    # for user_msg, bot_msg in history:

    # messages.append({"role": "user", "content": user_input})
    # print(chat_messages)
    # return chat_messages,output

def GenerateText(system_prompt,user_story):
    
    print(clientLLM)
    print(system_prompt)
    output = clientLLM.chat_completion(messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_story + " Story:"},
    ], max_tokens=1000,temperature=0.7).choices[0]["message"]["content"]

    return output

def GenerateImage(story):
    prompt = GenerateText(summarize_for_image,story)
    print(prompt)
    image= clientImage.text_to_image(prompt=prompt)
    image.save('RPG.png')
    return image

