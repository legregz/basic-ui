import pygame, json, os

from .Button import *
from .Text import *
from .utils import *

pygame.init()

global defaults, aliases, requirements

def importConfigFiles():
	global defaults, aliases, requirements

	#si le répertoire 'config' n'existe pas, il est créé
	if os.path.exists("config") == False:
		os.makedirs("config")

	#ouvre le fichier des paramètres par défaut, si il ne se trouve pas dans le répertoire du projet, il est importé depuis le répertoire 'config' du package
	try:
		with open("config/defaults.json") as f:
			defaults = json.load(f)
	except Exception:
		with open(f"{os.path.dirname(os.path.abspath(__file__))}/config/defaults.json") as f:
			defaults = json.load(f)

		with open("config/defaults.json", "w") as f:
			f.write(json.dumps(defaults, indent = 4))

	#ouvre le fichier des paramètres requis pour chaque type de composant
	with open(f"{os.path.dirname(os.path.abspath(__file__))}/config/requirements.json") as f:
		requirements = json.load(f)

	#ouvre le fichier des alias
	try:
		with open("config/aliases.json") as f:
			aliases = json.load(f)
	except Exception:
		with open(f"{os.path.dirname(os.path.abspath(__file__))}/config/aliases.json") as f:
			aliases = json.load(f)

		with open("config/aliases.json", "w") as f:
			f.write(json.dumps(aliases, indent = 4))

def setup(component, additionalSettings = {}):
	#vérifie si le paramêtre 'settings' existe
	if "settings" in component.settings.keys():
		#si le paramêtre 'settings' est un groupe de paramêtres, on ajoute chacun des paramêtres aux paramêtres du composant
		if type(component.settings["settings"]) == str:
			for key in settingsGroups[component.settings["settings"]].keys():
				try:
					component.settings[key]
				except:
					component.settings[key] = settingsGroups[component.settings["settings"]][key]

		#si le paramêtre 'settings' est une liste de groupe de paramêtre, on ajoute chacun des paramêtres de chaque groupe au paramêtres du composant
		elif type(component.settings["settings"]) == list:
			for settingsGroup in component.settings["settings"]:
				for key in settingsGroups[settingsGroup].keys():
					try:
						component.settings[key]
					except:
						component.settings[key] = settingsGroups[component.settings["settings"]][key]

		#on suppirme le paramêtre 'settings'
		del component.settings["settings"]

	#on ajoute tous les paramêtres présents dans les paramêtres définit dans la page
	for setting in additionalSettings.keys():
		component.settings[setting] = additionalSettings[setting]

	#pour tout les paramêtres requis mais vides, on applique la valeur par défaut
	for setting in requirements[component.name]:
		if not setting in component.settings.keys():
			component.settings[setting] = defaults[setting]

	component.size = Size(component)
	component.position = Position(component)

settingsGroups, components, sections = {}, {}, {}

def defineElements(elementsFileName):
	#ouvrir le fichier contenant les composants
	with open(elementsFileName) as f:
		elements = json.load(f)

	#pour chaque nom d'élément parmis ceux dans le fichier
	for element in elements.keys():
		if ":" in element:
			#si l'élément contient le séparateur ":", récupère le nom de la classe et celui de l'élément
			elementClassName, elementName = element.split(":")

			try:
				#vérifie si le type de composant existe
				eval(elementClassName)

			except Exception as e:
				#renvoie une erreur sinon
				print(f"{e} :\nLe composant {elementClassName} n'existe pas\n")

			else:
				if elementClassName == "Section":
					#si l'élément est une Section, l'ajoute au dictionnaire 'sections'
					sections[elementName] = eval(f"Section({elements[element]})")

				else:
					#sinon, ajoute l'élément au dictionnaire 'components'
					components[elementName] = eval(f"{elementClassName}({elements[element]})")
		else:
			#sinon, ajoute le groupe de paramêtres au dictionnaire 'settingsGroups'
			settingsGroups[element] = elements[element]

class Section:
	def __init__(self, elements):
		self.name = "Section"
		self.elements = elements

	def setElements(self, elements):
		self.screen = self.container.screen

		self.components = {}
		self.sections = {}
		self.settings = {}
		settings = {}
		
		#ouvrir le fichier contenant les composants
		if  type(elements) == str:
			with open(elements) as f:
				elements = json.load(f)

		#pour chaque nom d'élément parmis ceux dans le fichier
		for element in elements.keys():
			if ":" in element:
				#si l'élément contient le séparateur ":", récupère le nom de la classe et celui de l'élément
				elementClassName, elementName = element.split(":")

				try:
					#vérifie si le type de composant existe
					eval(elementClassName)

				except Exception as e:
					#renvoie une erreur sinon
					print(f"{e} :\nLe composant {elementClassName} n'existe pas\n")

				else:
					if elementClassName == "Section":
						#si l'élément est une Section, l'ajoute au dictionnaire 'sections'
						self.sections[elementName] = eval(f"Section({elements[element]})")

					else:
						#sinon, ajoute l'élément au dictionnaire 'self.components'
						self.components[elementName] = eval(f"{elementClassName}({elements[element]})")
						self.components[elementName].aliases = aliases

			else:
				if element in components.keys():
					#si le composant est défini, l'ajoute au dictionnaire 'self.components'
					self.components[element] = components[element]

				elif element in sections.keys():
					#si le composant est défini et est une section, l'ajoute au dictionnaire 'self.sections'
					self.sections[element] = sections[element]

				else:
					if element in requirements["Section"]:
						#si c'est un paramêtre requis, l'ajoute au dictionnaire 'settings'
						settings[element] = elements[element]

					else:
						#sinon renvoie une erreur
						print(f"Le composant {element} n'est pas défini\n")

		setup(self, settings)

		for componentName in self.components.keys():
			self.components[componentName].container = self
			setup(self.components[componentName])

		for sectionName in self.sections.keys():
			self.sections[sectionName].container = self
			self.sections[sectionName].setElements(self.sections[sectionName].elements)

	def show(self):
		for componentName in self.components.keys():
			self.components[componentName].show()

		for sectionName in self.sections.keys():
			self.sections[sectionName].show()

class Window(Section):
	class Container:
		def __init__(self, screen):
			self.size = WindowSize([screen.get_width(), screen.get_height()])
			self.position = WindowPosition([screen.get_width() / 2, screen.get_height() / 2])
			self.screen = screen

	def __init__(self, pageFileName, screen):
		self.name = "Section"
		self.screen = screen

		self.settings = {
			"size":["100%", "100%"],
			"position":["50%", "50%"]
		}

		self.container = self.Container(screen)

		self.setElements(pageFileName)