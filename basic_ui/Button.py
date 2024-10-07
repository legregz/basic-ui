import pygame

from .utils import *

class Button:
	def __init__(self, settings):
		self.settings = settings
		self.name = "Button"

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

		size = self.size.convert()

		size = list(map(adder(self.settings["margin"] * 2), size))

		pygame.draw.rect(
			self.container.screen,
			convertColor(self.settings["color"], self.aliases),
			[position[0] - size[0] // 2, position[1] - size[1] // 2, size[0], size[1]],
			border_radius = self.settings["border-radius"]
		)

		pygame.draw.rect(
			self.container.screen,
			self.convertColor(self.settings["border-color"]),
			[position[0] - size[0] // 2, position[1] - size[1] // 2, size[0], size[1]],
			self.settings["border-width"],
			self.settings["border-radius"]
		)

		self.container.screen.blit(text, [position[0]  - text.get_width() // 2, position[1] - text.get_height() // 2])