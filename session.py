import os
import uuid
import json
import datetime
import gradio as gr
from pathlib import Path

class SessionManager:
    """Manages saving, loading, and tracking RPG game sessions."""
    def __init__(self, app_state, registry_path="sessions_registry.json", sessions_dir="sessions"):
        self.registry_path = registry_path
        self.sessions_dir = sessions_dir
        self.session_id = None
        self.session_name = None
        self.session_type = None
        self.format_type = "Full session"  # Default format
        self.image_state = {}
        self.story = []
        self.app_state=app_state
        os.makedirs(sessions_dir, exist_ok=True)

    def generate_session_id(self):
        """Generate a unique session ID."""
        self.session_id = str(uuid.uuid4())
        return self.session_id
    
    def _load_registry(self):
        """Load the session registry from file."""
        try:
            with open(self.registry_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
    def _save_registry(self, registry):
        """Save the session registry to file."""
        with open(self.registry_path, "w") as f:
            json.dump(registry, f, indent=2)

    def update_registry(self):
        """
        Update the registry with a new or updated session.
        """
        registry = self._load_registry()
        
        registry = [entry for entry in registry 
                    if not (entry["name"] == self.session_name and entry["format"] == self.format_type)]
        
        # Add the new entry
        registry.append({
            "name": self.session_name,
            "id": self.session_id,
            "type": self.session_type,
            "format": self.format_type,  #currently only full session
            "timestamp": datetime.datetime.now().isoformat(),
            "image_state": self.image_state
        })
        
        self._save_registry(registry)

    def get_saved_sessions(self):
        """
        Get a list of all saved sessions.
        """
        registry = self._load_registry()
        return [(f"{entry['name']} ({entry['format']})", entry["id"]) for entry in registry]
    
    def set_session_data(self, name, story, session_type="rpg", image_state=None):
        """
        Set the current session data.
        """
        self.session_name = name
        self.story = story
        self.session_type = session_type
        self.image_state = image_state or {}
        
    def save_session(self):
        """
        Save a full session.
        """
        if not self.session_id:
            self.session_id = self.generate_session_id()
            
        session_dir = Path(self.sessions_dir) / self.session_id
        session_dir.mkdir(exist_ok=True)
        
        self.update_registry()
        
        story_path = session_dir / f"{self.session_name}.json"
        with open(story_path, "w") as file:
            json.dump(self.story, file, indent=4)
            
        gr.Info(f"Story saved as {self.session_name}.json in {session_dir}")
        return self.session_id
    
    def load_session(self, session_id):
        """
        Load a session.
        """
        try:
            registry = self._load_registry()
            entry = next((e for e in registry if e['id'] == session_id), None)
            
            if not entry:
                raise gr.Error("Session not found in registry")

            # Update current session state
            self.session_id = session_id
            self.session_name = entry['name']
            self.session_type = entry['type']
            self.format_type = entry['format']
            self.image_state = entry['image_state']
            
            session_path = Path(self.sessions_dir) / session_id

            if entry['format'] == "Full session":
                file_path = session_path / f"{entry['name']}.json"
                with open(file_path, "r") as file:
                    self.story = json.load(file)
                    self.app_state.story =  self.story
                    return  "", self.story, session_id, entry['image_state'], entry['type']

        except Exception as e:
            raise gr.Error(f"Failed to load session: {str(e)}")


        