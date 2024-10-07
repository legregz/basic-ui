import pygame

from utils import *

class Text():
	def __init__(self, settings):
		self.settings = settings

	def showComponent(self, screen):
		position = convertPosition(
			self.settings["position"].copy(),
			self.containerPosition,
			self.containerSize
		)

		text = pygame.font.SysFont(
			self.settings["font"],
			self.settings["font-size"]
		).render(
			self.settings["text"],
			True,
			convertColor(self.settings["font-color"], self.aliases)
		)

		screen.blit(text, [position[0] - text.get_width() // 2, position[1] - text.get_height() // 2])
