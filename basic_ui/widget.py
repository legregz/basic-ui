class Widget:
    def __init__(self, settings, requirements) -> None:
        self.settings = settings
        self.requirements = requirements
    
    def show(self) -> None:
        raise NotImplementedError("This method must be implemented in the child class")
    
    def setup(self):
        pass