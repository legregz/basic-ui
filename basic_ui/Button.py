import pygame

from .utils import *

class Button():
	def __init__(self, settings):
		self.settings = settings

	def showComponent(self, screen):
		position = convertPosition(
			self.settings["position"].copy(),
			self.container.settings["position"],
			self.container.settings["size"]
		)

		text = pygame.font.SysFont(
			self.settings["font"],
			self.settings["font-size"]
		).render(
			self.settings["text"],
			True,
			self.convertColor(self.settings["font-color"])
		)

		size = convertSize(
			self.settings["size"],
			self.containerSize,
			text.get_size()
		)

		size = list(map(adder(self.settings["margin"] * 2), size))

		pygame.draw.rect(
			screen,
			self.convertColor(self.settings["color"]),
			[position[0] - size[0] // 2, position[1] - size[1] // 2, size[0], size[1]],
			border_radius = self.settings["border-radius"]
		)

		pygame.draw.rect(
			screen,
			self.convertColor(self.settings["border-color"]),
			[position[0] - size[0] // 2, position[1] - size[1] // 2, size[0], size[1]],
			self.settings["border-width"],
			self.settings["border-radius"]
		)

		screen.blit(text, [position[0]  - text.get_width() // 2, position[1] - text.get_height() // 2])