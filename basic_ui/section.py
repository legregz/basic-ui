from .widget import Widget

class Section(Widget):
    def __init__(self, settings):
        self.settings = settings
        self.name = "Section"
        self.components = {}
        self.sections = {}