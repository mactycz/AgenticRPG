from abc import ABC, abstractmethod
class BaseInterface(ABC):
    def __init__(self, app_state):
        self.app_state = app_state
        self.container = None
        self.components = {}
        self._visible = True
        
    @abstractmethod
    def build(self):
        """Create interface components within Gradio context"""
        pass

    @abstractmethod
    def register_callbacks(self):
        """Connect event handlers"""
        pass

    @property
    def visible(self):
        return self._visible
    
    @visible.setter
    def visible(self, value):
        self._visible = value
        if self.container:
            self.container.visible = value