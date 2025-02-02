from local import LocalLlamaClient, LocalTransformersClient
import gradio as gr
from gradio.components import Image
import os
from prompts import *
from PIL import Image
import datetime
import json
import uuid
clientLLM = None
clientImage = None

SESSION_REGISTRY = "sessions_registry.json"

def generate_session_id():
    return str(uuid.uuid4())

def update_registry(session_name, session_id, format):
    try:
        with open(SESSION_REGISTRY, "r") as f:
            registry = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        registry = []
    registry = [entry for entry in registry 
                if not (entry["name"] == session_name and entry["format"] == format)] #removing the existing sessions with the same format and ind
    registry.append({
        "name": session_name,
        "id": session_id,
        "format": format,
        "timestamp": datetime.datetime.now().isoformat()
    })
    with open(SESSION_REGISTRY, "w") as f:
        json.dump(registry, f , indent=2)

def get_saved_sessions():
    try:
        with open(SESSION_REGISTRY, "r") as f:
            registry = json.load(f)
        return [(f"{entry['name']} ({entry['format']})",entry["id"]) for entry in registry]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

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

def api_call(msgs,selected_api,temperature = 0.7, max_tokens= 2000 , system_message = localPromptStory):
    api_call={
        "Huggingface API": lambda msgs:clientLLM.chat.completions.create(msgs,temperature=temperature,max_tokens=max_tokens).choices[0]["message"]["content"],
        "OpenAI": lambda msgs: clientLLM.chat.completions.create(model="gpt-4o-mini",messages=msgs, temperature=temperature, max_tokens=max_tokens).choices[0].message.content,
        "Anthropic": lambda msgs: clientLLM.messages.create(model="claude-3-5-sonnet-20241022",messages=msgs, temperature=temperature, max_tokens=max_tokens,system=system_message).content[0].text,
        "Local": lambda msgs: clientLLM.generate_response(msgs)
    }
    return api_call[selected_api](msgs)


def Chat(message,history,selected_api,abcd=False,automatic_image=False): # the automatic image is for conditional_generate_image to work, as I want two checkboxes in the same place - there must be a better way to do it, but it works for now
    messages = [{"role": "system", "content": localPromptStory + (abcd_options if abcd else "")}] if selected_api != "Anthropic" else [] #anthropic doesn't like system role 
    if len(history) == 1:
        messages.append({"role": "assistant", "content": initialize_story})
        messages.append({"role": "user", "content": localPromptStory+message})
        output = api_call(messages,selected_api)
        #clientLLM.chat_completion(messages,temperature=0.7,max_tokens=2000).choices[0]["message"]["content"]
        history.append([None,localPromptStory+message])
        history.append([localPromptStory+message,output])
    else:
        for user_msg, bot_msg in history:
            if user_msg is not None:
                messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
        messages.append({"role": "user", "content": message})
        output = api_call(messages,selected_api)
        #clientLLM.chat_completion(messages,temperature=0.7,max_tokens=2000)
        history.append((message,output))


    return output




def GenerateText(system_prompt,user_story,selected_api,max_tokens=500):
    messages = [{"role": "system", "content": system_prompt}] if selected_api != "Anthropic" else []
    messages.append({"role": "user", "content": user_story + " Story:"})
    output = api_call(messages,selected_api=selected_api,temperature=0.7,max_tokens=max_tokens,system_message=system_prompt)
    return output

def GenerateImage(story,selected_api,session_id,style=""):
    story = story[-1][-1]
    prompt = GenerateText(summarize_for_image,story,selected_api)
    if style != "":
        prompt = prompt+ f' Generate the image in {style} style.'
    print(f"Image prompt {prompt}")
    image= clientImage.text_to_image(prompt=prompt)
    date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    image_dir = f"session/{session_id}/images"
    os.makedirs(image_dir, exist_ok=True)
    image.save(f"{image_dir}/image-{date}.png")
    return image

def conditional_generate_image(story,auto_generate,selected_api,session_id ,style=""):
    if auto_generate:
        if story[-1][1] is not None:
            return GenerateImage(story,selected_api,session_id,style)
    return "helpers/placeholder.png" 

def summarize_and_save(story,name,selected_api,format,session_id):
    
    
    
    if format == "Session summary":
        session_id = generate_session_id()
        story_dir = f"session/{session_id}"
        os.makedirs(story_dir,exist_ok=True)
        update_registry(name, session_id,format)
        gr.Info("Generating summary, it might take a minute")
        story_string = "\n\n".join(
            f"user: {user_msg}\nnarrator: {narrator_msg}"
            for user_msg, narrator_msg in story)
        output = GenerateText(summarize_for_future,story_string,selected_api,1000)
        print(output)
        with open(f"{story_dir}/{name}.txt", "w+") as file:
            file.write(output)
    
    elif format == "Full session":
        story_dir = f"session/{session_id}"
        os.makedirs(story_dir,exist_ok=True)
        update_registry(name, session_id,format)
        story_json = json.dumps(story, indent=4)
        with open(f"{story_dir}/{name}.json", "w+") as file:
            file.write(story_json)
    else:
        print("Incorrect format")

    gr.Info(f"Story saved as story-{name}.{'txt' if format=='Session summary' else 'json'} in stories folder")

def load_story(session_id):
    
    try:
        with open(SESSION_REGISTRY, "r") as f:
            registry = json.load(f)
        entry = next((e for e in registry if e['id'] == session_id), None)
        print(entry)
        print(entry['name'])
        print(entry['id'])
        if not entry:
            raise gr.Error("Session not found")
        
        if not session_id:
            raise gr.Error("Session not found")

        session_path = f"session/{session_id}"
        print(f"{session_path}/{entry['name']} {entry['format']}")
        if entry['format'] == "Session summary":
            with open(f"{session_path}/{entry['name']}.txt", "r") as file:
                story = f"Story so far: {file.read()}"
                print(story)
                return story, [(None,story)], session_id
            
        elif entry['format'] == "Full session":
            with open(f"{session_path}/{entry['name']}.json", "r") as file:
                story = json.load(file)
                print(story)
                return "",story , session_id

    except Exception as e:
        raise gr.Error(f"No saved session found: {str(e)}")
    



