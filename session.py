
import uuid
import json
import gradio as gr
import json
import datetime
import os
from prompts import summarize_for_future
from app import generate_text
SESSION_REGISTRY = "sessions_registry.json"

def generate_session_id():
    return str(uuid.uuid4())

def update_registry(session_name, session_id, session_type, format, image_state):
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
        "type": session_type,
        "format": format,
        "timestamp": datetime.datetime.now().isoformat(),
        "image_state": image_state
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
    
def summarize_and_save(story,name,selected_api,session_type,format,image_state,session_id):
    if format == "Session summary":
        session_id = generate_session_id()
        story_dir = f"sessions/{session_id}"
        os.makedirs(story_dir,exist_ok=True)
        update_registry(name, session_id,session_type,format,image_state)
        gr.Info("Generating summary, it might take a minute")
        story_string = "\n\n".join(
            f"user: {user_msg}\nnarrator: {narrator_msg}"
            for user_msg, narrator_msg in story)
        output = generate_text(summarize_for_future,story_string,selected_api,1000)
        with open(f"{story_dir}/{name}.txt", "w+") as file:
            file.write(output)
    
    elif format == "Full session":
        story_dir = f"sessions/{session_id}"
        os.makedirs(story_dir,exist_ok=True)
        update_registry(name, session_id,session_type,format,image_state)
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
        if not entry:
            raise gr.Error("Session not found")
        
        if not session_id:
            raise gr.Error("Session not found")
        session_type = entry['type']
        session_path = f"sessions/{session_id}"
        if entry['format'] == "Session summary":
            with open(f"{session_path}/{entry['name']}.txt", "r") as file:
                story = f"Story so far: {file.read()}"
                return story, [(None,story)], session_id, entry['image_state'],session_type
            
        elif entry['format'] == "Full session":
            with open(f"{session_path}/{entry['name']}.json", "r") as file:
                story = json.load(file)
                return "",story , session_id, entry['image_state'], session_type

    except Exception as e:
        raise gr.Error(f"No saved session found: {str(e)}")
    


def update_session_type(session_type):
    return session_type


    