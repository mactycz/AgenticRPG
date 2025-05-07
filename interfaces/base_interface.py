from abc import ABC, abstractmethod

class BaseInterface(ABC):
    def __init__(self, app_state, navigate_fn=None,tabs_component=None):
        self.app_state = app_state
        self.navigate_fn = navigate_fn  # Function to navigate between tabs
        self.tabs_component = tabs_component
        self.components = {}
        
    @abstractmethod
    def build(self):
        """Build interface components"""
        pass

    @abstractmethod
    def register_callbacks(self, tabs_component):
        """
        Connect event handlers
        
        Parameters:
        - tabs_component: The Gradio Tabs component for navigation
        """
        pass
        
