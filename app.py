from local import LocalLlamaClient, LocalTransformersClient
import gradio as gr
from gradio.components import Image
import os
from prompts import *
from PIL import Image
from diffusers import DiffusionPipeline
import datetime

clientLLM = None
clientImage = None
def add_key_and_show_interface(api_choice, provided_api_key,provided_api_token,model_name_llm, model_name_image):
    global api_key, api_token
    if provided_api_key:
        api_key = provided_api_key
    elif provided_api_token:
        api_token = provided_api_token
    else:
        api_key = ""
    print(api_choice,provided_api_key,provided_api_token)
    connect_to_api(api_choice,provided_api_key,provided_api_token,model_name_llm,model_name_image)
    if provided_api_key:
        return gr.update(visible=True),gr.update(visible=False)
    if provided_api_token:
        return gr.update(visible=True),gr.update(visible=False)
    return gr.update(visible=False),gr.update(visible=True)

def update_placeholders(option,auth,keys):
    if auth=="Enviromental variable token":
        return gr.update(value=keys[option])


def connect_to_api(api,auth,key,model_name_llm,model_name_image):
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

    elif api == "Local":
        print("local")
        try:
            if "gguf" in model_name_llm:
                print("llama")
                clientLLM = LocalLlamaClient(model_name_llm)
            else :
                print("transformers")
                clientLLM = LocalTransformersClient(model_name_llm)
            print(f"Local model loaded: {model_name_llm}")

        except Exception as e:
            print(f"Error loading local model: {str(e)}")



def Client(model):
    from huggingface_hub import InferenceClient
    global client 
    client= InferenceClient(
        model
    )
    return client

def Chat(message,history,selected_api,abcd=False,automatic_image=False): # the automatic image is for conditional_generate_image to work, as I want two checkboxes in the same place - there must be a better way to do it, but it works for now
    api_call={
        "Huggingface API": lambda msgs:clientLLM.chat_completion(msgs,temperature=0.7,max_tokens=2000).choices[0]["message"]["content"],
        "OpenAI": lambda msgs: clientLLM.chat.completions.create(model="gpt-4o-mini",messages=msgs, temperature=0.7, max_tokens=2000).choices[0].message.content,
        "Anthropic": lambda msgs: clientLLM.messages.create(model="claude-3-5-sonnet-20241022",messages=msgs, temperature=0.7, max_tokens=2000,system=localPromptStory + (abcd_options if abcd else "")).content[0].text,
        "Local": lambda msgs: clientLLM.generate_response(msgs)
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
        history.append((message,output))


    return output




def GenerateText(system_prompt,user_story):
    output = clientLLM.chat_completion(messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_story + " Story:"},
    ],temperature=0.7,max_tokens=500).choices[0]["message"]["content"]

    return output

def GenerateImage(story,style=""):
    story = story[-1][-1]
    prompt = GenerateText(summarize_for_image,story)
    if style != "":
        prompt = prompt+ f' Generate the image in {style} style.'
    print(f"Image prompt {prompt}")
    image= clientImage.text_to_image(prompt=prompt)
    date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    image.save(f"images/image-{date}.png")

    
    return image

def conditional_generate_image(story,auto_generate, style=""):
    print(f"Auto generate on: {auto_generate}")
    if auto_generate:
        if story[-1][1] is not None:
            print(f"Player provided the story")
            return GenerateImage(story,style)
        
    return "helpers/placeholder.png" 