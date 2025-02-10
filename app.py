from local import LocalLlamaClient, LocalTransformersClient
import gradio as gr
from gradio.components import Image
import os
from prompts import *
from PIL import Image
import datetime
from openai import OpenAI
import anthropic
clientLLM = None
clientImage = None

def add_key_and_show_interface(api_llm,auth_llm, provided_api_key_llm,model_name_llm,provider_llm,api_image,auth_image, provided_api_key_image_image,provider_image):
    global api_key
    if provided_api_key_llm=="":
        gr.Info("Please provide an API key").update(visible=True)
        return gr.update(visible=False),gr.update(visible=True)
    if auth_llm == "Enviromental variable token":
        provided_api_key_llm = os.environ.get(provided_api_key_llm)
    if auth_image == "Enviromental variable token":
        provided_api_key_image_image = os.environ.get(provided_api_key_image_image)
    clientLLM = connect_to_api_llm(api_llm,auth_llm,provided_api_key_llm,model_name_llm,provider_llm)
    clientImage = connect_to_api_image(api_image,auth_image,provided_api_key_image_image,provider_image)
    return gr.update(visible=True),gr.update(visible=False)
    

def update_placeholders_llm(option,auth,keys,model_list,default_models):
    if auth=="Enviromental variable token":
        return gr.update(value=keys[option]),gr.update(choices = model_list[option]),gr.update(value=default_models[option])
    else:
        return gr.update(value=""),gr.update(choices = model_list[option]),gr.update(value=default_models[option])
    

def connect_to_api_llm(api,auth,key,model_name,provider=""):
    global clientLLM
    print(key)
    if auth == "Enviromental variable token":
        key = os.environ.get(key)
    if api == "Huggingface API":
        if provider=="" or provider == "HF Inference API":
            base_url = "https://router.huggingface.co/hf-inference/v1"
        else:
            base_url = f"https://router.huggingface.co/{provider}"
        clientLLM = OpenAI(
            base_url=base_url,
            api_key=key)
    elif api =="OpenAI":
        clientLLM = OpenAI(api_key=key)
    elif api == "Anthropic":
        clientLLM = anthropic.Anthropic(api_key=key)
    elif api == "Local":
        try:
            if "gguf" in model_name:
                print("llama")
                clientLLM = LocalLlamaClient(model_name)
            else :
                print("transformers")
                clientLLM = LocalTransformersClient(model_name)
            print(f"Local model loaded: {model_name}")
        except Exception as e:
            print(f"Error loading local model: {str(e)}")
    print(clientLLM)

def connect_to_api_image(api,auth,key,provider=""):
    global clientImage
    if auth == "Enviromental variable token":
        key = os.environ.get(key)
    if api == "Huggingface API":
        from huggingface_hub import InferenceClient
        clientImage = InferenceClient(
            provider=provider,
            api_key=key)
    elif api =="OpenAI":
        clientImage = OpenAI()
    elif api == "Local":
        print("TODO")
        clientImage = None

def api_call_llm(msgs,selected_api, model_name, temperature = 0.7, max_tokens= 2000 , system_message = localPromptStory):
    api_call={
        "Huggingface API": lambda msgs:clientLLM.chat.completions.create(messages=msgs,model = model_name,temperature=temperature,max_tokens=max_tokens).choices[0].message.content,
        "OpenAI": lambda msgs: clientLLM.chat.completions.create(model=model_name,messages=msgs, temperature=temperature, max_tokens=max_tokens).choices[0].message.content,
        "Anthropic": lambda msgs: clientLLM.messages.create(model=model_name,messages=msgs, temperature=temperature, max_tokens=max_tokens,system=system_message).content[0].text,
        "Local": lambda msgs: clientLLM.generate_response(msgs)
    }
    return api_call[selected_api](msgs)

def api_call_image(prompt,selected_api,model):
    api_call = {
        "OpenAI" : lambda prompt: OpenAI.images.generate({prompt:prompt,model:model}),
        "Huggingface" : lambda prompt : clientImage.text_to_image(prompt=prompt,model=model)
    }
    return api_call[selected_api](prompt)

def chat(message,history,selected_api,model_name,temperature,abcd=False,automatic_image=False): # the automatic image is for conditional_generate_image to work, as I want two checkboxes in the same place - there must be a better way to do it, but it works for now
    messages = [{"role": "system", "content": localPromptStory + (abcd_options if abcd else "")}] if selected_api != "Anthropic" else [] #anthropic doesn't like system role 
    if len(history) == 1:
        messages.append({"role": "assistant", "content": initialize_story})
        messages.append({"role": "user", "content": localPromptStory+message})
        output = api_call_llm(messages,selected_api,model_name,temperature)
        history.append([None,localPromptStory+message])
        history.append([localPromptStory+message,output])
    else:
        for user_msg, bot_msg in history:
            if user_msg is not None:
                messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
        messages.append({"role": "user", "content": message})
        output = api_call_llm(messages,selected_api,model_name,temperature)
        history.append((message,output))
    return output

def generate_text(system_prompt,user_story,model_name,selected_api,temperature,max_tokens=500):
    messages = [{"role": "system", "content": system_prompt}] if selected_api != "Anthropic" else []
    messages.append({"role": "user", "content": user_story + " Story:"})
    output = api_call_llm(messages,selected_api,model_name,temperature=temperature,max_tokens=max_tokens,system_message=system_prompt)
    return output

def generate_image(story,selected_api_llm,selected_api_image,session_id,image_state,model_name_llm,model_name_image,temperature,style=""):
    story = story[-1][-1]
    prompt = generate_text(summarize_for_image,story,model_name_llm,selected_api_llm,temperature)
    if style != "":
        prompt = prompt+ f' Generate the image in {style} style.'
    image= api_call_image[selected_api_image](prompt,model_name_image)
    date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    image_dir = f"sessions/{session_id}/images"
    os.makedirs(image_dir, exist_ok=True)
    image.save(f"{image_dir}/image-{date}.png")
    image_path = f"{image_dir}/image-{date}.png"
    image_state = update_image_state(image_state,session_id,"Add",image_path)
    return image_path, image_state

def conditional_generate_image(story,auto_generate,selected_api_llm,selected_api_image,session_id,image_state,model_name_llm,model_name_image,temperature,style=""):
    if auto_generate and story and story[-1][1] is not None:
        return generate_image(story,selected_api_llm,selected_api_image,session_id,image_state,model_name_llm,model_name_image,temperature,style)
    else :
        return image_state["current_image_path"],image_state


def get_images(session_id):
    image_dir = f"sessions/{session_id}/images"
    images = sorted(os.listdir(image_dir))
    return images

def update_image_state(image_state,session_id,action,image_path=""):
    images  = get_images(session_id)
    if action == "Add":
        image_state["image_count"] += 1
        image_state["current_image_index"]  = image_state["image_count"]
        image_state["current_image_path"] = image_path
        return image_state
    elif action == "previous":
        if image_state["current_image_index"] > 1:
            image_state["current_image_index"] -= 1
            image_state["current_image_path"] = f"sessions/{session_id}/images/{images[image_state['current_image_index']-1]}"
            return image_state
        else:
            return image_state
    elif action == "next":
        if image_state["current_image_index"] < image_state["image_count"]:
            image_state["current_image_index"] += 1
            image_state["current_image_path"] = f"sessions/{session_id}/images/{images[image_state['current_image_index']-1]}"
            return image_state
        else:
            return image_state
        

def update_image(image_state):
    return image_state['current_image_path'],f"{image_state['current_image_index']}/{image_state['image_count']}"

