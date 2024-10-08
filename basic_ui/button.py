import pygame

from .widget import Widget

class Button(Widget):
	def __init__(self, settings) -> None:
		self.settings = settings
		self.name = "Button"