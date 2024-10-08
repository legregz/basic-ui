import pygame

from .widget import Widget

class Label(Widget):
    def __init__(self, settings):
        self.settings = settings
        self.name = "Label"