import pygame

from .utils import *

class Text:
	def __init__(self, settings):
		self.settings = settings
		self.name = "Text"

	def show(self):
		position = self.position.convert()

		text = pygame.font.SysFont(
			self.settings["font"],
			self.settings["font-size"]
		).render(
			self.settings["text"],
			True,
			convertColor(self.settings["font-color"], self.aliases)
		)

		self.container.screen.blit(text, [position[0] - text.get_width() // 2, position[1] - text.get_height() // 2])
