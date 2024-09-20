import pygame, json, os, importlib_resources
pygame.init()

os.chdir(".")

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
        position : list
        size : list
        containerPosition : list (in pixels)
        containerSize : list (in pixels)"""
    position = convertPosition(position, containerPosition, containerSize)
    size = convertSize(size, containerSize)

    return [position[0], position[1], size[0], size[1]]

def convertPosition(position, containerPosition, containerSize):
    """convertPosition : fonction permettant de convertir une position depuis le format utilisé dans la page json en position en pixels
    args:
        position : list
        containerPosition : list (in pixels)
        containerSize : list (in pixels)"""
    for i in range(2):
        if position[i].endswith("%"):
            position[i] = (containerPosition[i] + containerSize[i] / 100) * int(position[i][0:-1])
        elif position[i].endswith("px"):
            position[i] = containerPosition[i] + int(position[i][0:-2])

    return position

def convertSize(size, containerSize):
    """convertSize : fonction permettant de convertir une size depuis le format utilisé dans la page json en size en pixels
    args:
        size : list
        containerSize : list (in pixels)"""
    for i in range(2):
        if size[i].endswith("%"):
            size[i] = containerSize[i] / 100 * int(size[i][0:-1])
        elif size[i].endswith("px"):
            size[i] = int(size[i][0:-2])

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

settingsGroups, components, divs = {}, {}, {}

def setElements(elementsFileName):
    #ouvrir le fichier contenant les composants
    with open(elementsFileName) as f:
        elements = json.load(f)

    #pour chaque nom de élément parmis ceux dans le fichier
    for elementName in elements.keys():
        #pour chaque élément contenu dans le nom du composant
        for elementClassName in elements[elementName].keys():
            try:
                #vérifie si l'élément est un composant
                eval(elementClassName)
            except:
                #sinon test si l'élément est une div. si oui, ajoute l'élément à la liste des divs
                if elementClassName in elements.keys():
                    divs[elementName] = elements[elementName]
                #ou un groupe de paramètres
                else:
                    settingsGroups[elementName] = elements[elementName]
            else:
                #sinon créé un composant en évaluant la classe définit par elementClassName
                components[elementName] = eval(f"{elementClassName}({elements[elementName][elementClassName]})")

class Page:
    def __init__(self, screen, pageFileName):
        file = open(pageFileName)
        data = eval(file.read())
        file.close()

        self.components = {}
        size = screen.get_size()
        self.screen = screen

        #pour tout les noms de composants de la page
        for componentName in data.keys():
            try:
                #test si c'est un composant
                components[componentName]
            except:
                try:
                    #test si c'est une div
                    divs[componentName]
                except:
                    pass
                else:
                    #si oui, tout les composants de la div sont ajoutés aux composants de la page
                    for divComponentName in divs[componentName].keys():
                        self.components[componentName] = components[divComponentName]
            else:
                #si oui, setup de chaque composant
                self.components[componentName] = components[componentName]
                self.components[componentName].setup(data[componentName])
                self.components[componentName].setContainer(size)

    def globalSetup(self, componentClassName, additionalSettings):
        if self.settings["settings"]:
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

    def setContainer(self, size):
        self.containerSize = size
        self.containerPosition = [0, 0]

    def show(self):
        for componentName in self.components.keys():
            self.components[componentName].showComponent(self.screen)

class Button(Page):
    def __init__(self, settings):
        self.settings = settings

    def setup(self, additionalSettings = {}):
        self.globalSetup("Button", additionalSettings)

    def showComponent(self, screen):
        position = convertPosition(self.settings["position"].copy(), self.containerPosition, self.containerSize)
        size = convertSize(self.settings["size"].copy(), self.containerSize)

        pygame.draw.rect(screen, convertColor(self.settings["color"]), [position[0] - size[0] // 2, position[1] - size[1] // 2, size[0], size[1]], border_radius = self.settings["border-radius"])
        pygame.draw.rect(screen, convertColor(self.settings["color"]), [position[0] - size[0] // 2, position[1] - size[1] // 2, size[0], size[1]], self.settings["border-width"], self.settings["border-radius"])
        text = pygame.font.SysFont(self.settings["font"], self.settings["font-size"]).render(self.settings["text"], True, convertColor(self.settings["font-color"]))
        screen.blit(text, [position[0]  - text.get_width() // 2, position[1] - text.get_height() // 2])

class Text(Page):
    def __init__(self, settings):
        self.settings = settings

    def setup(self, additionalSettings = {}):
        self.globalSetup("Text", additionalSettings)

    def showComponent(self, screen):
        position = convertPosition(self.settings["position"].copy(), self.containerPosition, self.containerSize)
        text = pygame.font.SysFont(self.settings["font"], self.settings["font-size"]).render(self.settings["text"], True, convertColor(self.settings["font-color"]))
        screen.blit(text, [position[0] - text.get_width() // 2, position[1] - text.get_height() // 2])
