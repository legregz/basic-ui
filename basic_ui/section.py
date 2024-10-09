from .widget import Widget

class Section(Widget):
    def __init__(self, elements, settings, requirements) -> None:
        super().__init__(settings, requirements)
        self.components = {}
        self.sections = {}