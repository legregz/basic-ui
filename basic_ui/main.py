import pygame, json, os, importlib_resources
pygame.init()

global defaults, aliases, requirements

def adder(number):
	def add(value):
		return number + value
	return add

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
		with importlib_resources.open_text("basic_ui", "config/defaults.json") as f:
			defaults = json.load(f)

		with open("config/defaults.json", "w") as f:
			f.write(json.dumps(defaults, indent = 4))

	#ouvre le fichier des paramètres requis pour chaque type de composant
	with importlib_resources.open_text("basic_ui", "config/requirements.json") as f:
		requirements = json.load(f)

	#ouvre le fichier des alias
	try:
		with open("config/aliases.json") as f:
			aliases = json.load(f)
	except Exception:
		with importlib_resources.open_text("basic_ui", "config/aliases.json") as f:
			aliases = json.load(f)

		with open("config/aliases.json", "w") as f:
			f.write(json.dumps(aliases, indent = 4))

def convertRect(position, size, containerPosition, containerSize):
	"""convertRect : fonction permettant de convertir une position et une size depuis le format utilisé dans la page json en position et size en pixels
	args:
		position : list (pixels or %)
		size : list (pixels or %)
		containerPosition : list (pixels)
		containerSize : list (pixels)"""
	position = convertPosition(position, containerPosition, containerSize)
	size = convertSize(size, containerSize)

	return [position[0], position[1], size[0], size[1]]

def convertPosition(position, containerPosition, containerSize):
	"""convertPosition : fonction permettant de convertir une position depuis le format utilisé dans la page json en position en pixels
	args:
		position : list (pixels or %)
		containerPosition : list (pixels)
		containerSize : list (pixels)"""
	for i in range(2):
		if position[i].endswith("%"):
			position[i] = (containerPosition[i] + containerSize[i] / 100) * int(position[i][0:-1])
		elif position[i].endswith("px"):
			position[i] = containerPosition[i] + int(position[i][0:-2])

	return position

def convertSize(sizeArg, containerSize, autoSize = []):
	"""convertSize : fonction permettant de convertir une size depuis le format utilisé dans la page json en size en pixels
	args:
	size : list (pixels or %)
	containerSize : list (pixels)"""
	if sizeArg != "auto":
		size = sizeArg.copy()
		for i in range(2):
			if size[i].endswith("%"):
				size[i] = containerSize[i] / 100 * int(size[i][0:-1])
			elif size[i].endswith("px"):
				size[i] = int(size[i][0:-2])

		if autoSize[0] > size[0]:
			size[0] = autoSize[0]

		if autoSize[1] > size[1]:
			size[1] = autoSize[1]

	else:
		size = autoSize

	return size

def convertColor(color):
	"""convertColor : fonction permettant de convertir une color depuis le format utilisé dans la page json en color RVB"""
	if color in aliases.keys():
		color = aliases[color]

	if len(color) == 1:
		color = color * 6
	elif len(color) == 3:
		color = color[0] * 2 + color[1] * 2 + color[2] * 2

	return [int(f"0x{color[0:2]}", 16), int(f"0x{color[2:4]}", 16), int(f"0x{color[4:6]}", 16)]

settingsGroups, components, sections = {}, {}, {}

def setElements(elementsFileName):
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
		self.setElements(elements)

	def setScreen(self, screen):
		self.screen = screen

	def setElements(self, elements):
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

			else:
				if element in components.keys():
					#si le composant est défini, l'ajoute au dictionnaire 'self.components'
					self.components[element] = components[element]

				else:
					if element in requirements["Section"]:
						#si c'est un paramêtre requis, l'ajoute au dictionnaire 'settings'
						settings[element] = elements[element]

					else:
						#sinon renvoie une erreur
						print(f"Le composant {element} n'est pas défini\n")

		self.globalSetup("Section", settings)

		for componentName in self.components:
			self.components[componentName].setup()
			self.components[componentName].setContainer(self)

	def globalSetup(self, componentClassName, additionalSettings):
		#vérifie si le paramêtre 'settings' existe
		if "settings" in self.settings.keys():
			#si le paramêtre 'settings' est un groupe de paramêtres, on ajoute chacun des paramêtres aux paramêtres du composant
			if type(self.settings["settings"]) == str:
				for key in settingsGroups[self.settings["settings"]].keys():
					try:
						self.settings[key]
					except:
						self.settings[key] = settingsGroups[self.settings["settings"]][key]

			#si le paramêtre 'settings' est une liste de groupe de paramêtre, on ajoute chacun des paramêtres de chaque groupe au paramêtres du composant
			elif type(self.settings["settings"]) == list:
				for settingsGroup in self.settings["settings"]:
					for key in settingsGroups[settingsGroup].keys():
						try:
							self.settings[key]
						except:
							self.settings[key] = settingsGroups[self.settings["settings"]][key]

			#on suppirme le paramêtre 'settings'
			del self.settings["settings"]

		#on ajoute tous les paramêtres présents dans les paramêtres définit dans la page
		for setting in additionalSettings.keys():
			self.settings[setting] = additionalSettings[setting]

		#pour tout les paramêtres requis mais vides, on applique la valeur par défaut
		for setting in requirements[componentClassName]:
			if not setting in self.settings.keys():
				self.settings[setting] = defaults[setting]

	def setContainer(self, container):
		self.container = container

	def show(self):
		for componentName in self.components.keys():
			self.components[componentName].showComponent(self.screen)

class Window(Section):
	def __init__(self, pageFileName, screen):
		self.setScreen(screen)
		self.setElements(pageFileName)

class Button(Section):
	def __init__(self, settings):
		self.settings = settings

	def setup(self, additionalSettings = {}):
		self.globalSetup("Button", additionalSettings)

	def showComponent(self, screen):
		position = convertPosition(self.settings["position"].copy(), self.container.settings["position"], self.container.settings["size"])
		text = pygame.font.SysFont(self.settings["font"], self.settings["font-size"]).render(self.settings["text"], True, convertColor(self.settings["font-color"]))
		size = convertSize(self.settings["size"], self.containerSize, text.get_size())
		size = list(map(adder(self.settings["margin"] * 2), size))

		pygame.draw.rect(screen, convertColor(self.settings["color"]), [position[0] - size[0] // 2, position[1] - size[1] // 2, size[0], size[1]], border_radius = self.settings["border-radius"])
		pygame.draw.rect(screen, convertColor(self.settings["border-color"]), [position[0] - size[0] // 2, position[1] - size[1] // 2, size[0], size[1]], self.settings["border-width"], self.settings["border-radius"])
		screen.blit(text, [position[0]  - text.get_width() // 2, position[1] - text.get_height() // 2])

class Text(Section):
	def __init__(self, settings):
		self.settings = settings

	def setup(self, additionalSettings = {}):
		self.globalSetup("Text", additionalSettings)

	def showComponent(self, screen):
		position = convertPosition(self.settings["position"].copy(), self.containerPosition, self.containerSize)
		text = pygame.font.SysFont(self.settings["font"], self.settings["font-size"]).render(self.settings["text"], True, convertColor(self.settings["font-color"]))
		screen.blit(text, [position[0] - text.get_width() // 2, position[1] - text.get_height() // 2])
