from abc import ABC, abstractmethod
class BaseInterface(ABC):
    def __init__(self, app_state):
        self.app_state = app_state
        self.container = None
        self.components = {}
        
    @abstractmethod
    def build(self):
        """Create interface components within Gradio context"""
        pass

    @abstractmethod
    def register_callbacks(self):
        """Connect event handlers"""
        pass

    def get_visibility(self):
        """Return initial visibility state"""
        return True