from loadModel import loadModel
import gradio as gr
import os
#API key interface - disappears after providing api and shows main interface
from prompts import *
from PIL import Image
from diffusers import DiffusionPipeline
clientLLM = None
clientImage = None
def add_key_and_show_interface(api_choice, provided_api_key,provided_api_token,model_name_llm):
    global api_key, api_token
    if provided_api_key:
        api_key = provided_api_key
    elif provided_api_token:
        api_token = provided_api_token
    else:
        api_key = ""
    print(api_choice,provided_api_key,provided_api_token)
    connect_to_api(api_choice,provided_api_key,provided_api_token,model_name_llm)
    if provided_api_key:
        return gr.update(visible=True),gr.update(visible=False)
    if provided_api_token:
        return gr.update(visible=True),gr.update(visible=False)
    return gr.update(visible=False),gr.update(visible=True)

def update_placeholders(option,auth,keys):
    if auth=="Enviromental variable token":
        return gr.update(value=keys[option])


def connect_to_api(api,auth,key,model_name_llm,model_name_image="stabilityai/stable-diffusion-3.5-large"):
    global clientLLM
    global clientImage
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
                login(token)
            except:
                print("invalid token or token name")
        elif token=="" and api_key=="":
            print("No auth method provided. This shouldn't be possible")
        clientLLM=Client(model_name_llm)
        clientImage=Client(model_name_image)
        print(f"MODELS LOADED {model_name_llm}, {model_name_image}")



    elif api =="OpenAI":
        from openai import OpenAI
        if auth=="API key":
            print("Provided api key")
            try:
                OpenAI.api_key = api_key
            except:
                print("invalid api key")
        elif auth=="Enviromental variable token":
            print("Token provided: "+key)
        elif token=="" and api_key=="":
            print("No auth method provided. This shouldn't be possible")
        clientLLM = OpenAI()
        clientImage = OpenAI()
        print("openai")




    elif api == "Anthropic":
        import anthropic
        if auth=="API key":
            print("Provided api key")
            try:
                OpenAI.api_key = api_key
            except:
                print("invalid api key")
        elif auth=="Enviromental variable token":
            print("Token provided: "+key)
        elif token=="" and api_key=="":
            print("No auth method provided. This shouldn't be possible")
        clientLLM = anthropic.Anthropic()
        print("anth")
    elif api=="local":
        print("local")



def Client(model):
    from huggingface_hub import InferenceClient
    global client 
    client= InferenceClient(
        model
    )
    return client

def Chat(message,history,selected_api,abcd=False):
    api_call={
        "Huggingface API": lambda msgs:clientLLM.chat_completion(msgs,temperature=0.7,max_tokens=2000).choices[0]["message"]["content"],
        "OpenAI": lambda msgs: clientLLM.chat.completions.create(model="gpt-4o-mini",messages=msgs, temperature=0.7, max_tokens=2000).choices[0].message.content,
        "Anthropic": lambda msgs: clientLLM.messages.create(model="claude-3-5-sonnet-20241022",messages=msgs, temperature=0.7, max_tokens=2000,system=localPromptStory + (abcd_options if abcd else "")).content[0].text,
        "Local": lambda msgs: print(msgs) #placeholder for now
    }

    messages = [{"role": "system", "content": localPromptStory + (abcd_options if abcd else "")}] if selected_api != "Anthropic" else [] #anthropic doesn't like system role 
    if len(history) == 1:
        messages.append({"role": "assistant", "content": initialize_story})
        messages.append({"role": "user", "content": localPromptStory+message})
        output = api_call[selected_api](messages)
        #clientLLM.chat_completion(messages,temperature=0.7,max_tokens=2000).choices[0]["message"]["content"]
        history.append([None,localPromptStory+message])
        history.append([localPromptStory+message,output])
    else:
        for user_msg, bot_msg in history:
            if user_msg is not None:
                messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
        messages.append({"role": "user", "content": message})



        output = api_call[selected_api](messages)
        #clientLLM.chat_completion(messages,temperature=0.7,max_tokens=2000)
        print(output)
        history.append((message,output))
    return output




def GenerateText(system_prompt,user_story):
    output = clientLLM.chat_completion(messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_story + " Story:"},
    ],temperature=0.7,max_tokens=500).choices[0]["message"]["content"]

    return output

def GenerateImage(story):
    story = story[-1][-1]
    prompt = GenerateText(summarize_for_image,story)
    print(prompt)
    image= clientImage.text_to_image(prompt=prompt)
    image.save('RPG.png')
    return image

