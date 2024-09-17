import pygame
pygame.init()

#ouvre le fichier des paramètres par défaut
file = open("default.json")
default = eval(file.read())
file.close()
#ouvre le fichier des paramètres requis pour chaque type de composant
file = open("requirements.json")
requirements = eval(file.read())
file.close()
#ouvre le fichier des alias
file = open("aliases.json")
aliases = eval(file.read())
file.close()

settingsGroups, components, divs = {}, {}, {}
    
def convertRect(position, size, containerPosition, containerSize):
    position = convertPosition(position, containerPosition, containerSize)
    size = convertSize(size, containerSize)

    return [position[0], position[1], size[0], size[1]]

def convertPosition(position, containerPosition, containerSize):
    for i in range(2):
        if position[i].endswith("%"):
            position[i] = (containerPosition[i] + containerSize[i] / 100) * int(position[i][0:-1])
        elif position[i].endswith("px"):
            position[i] = containerPosition[i] + int(position[i][0:-2])

    return position

def convertSize(size, containerSize):
    for i in range(2):
        if size[i].endswith("%"):
            size[i] = containerSize[i] / 100 * int(size[i][0:-1])
        elif size[i].endswith("px"):
            size[i] = int(size[i][0:-2])

    return size

def convertColor(color):
    if color in aliases.keys():
        color = aliases[color]

    if len(color) == 1:
        color = color * 6
    elif len(color) == 3:
        color = color[0] * 2 + color[1] * 2 + color[2] * 2

    return [int(f"0x{color[0:2]}", 16), int(f"0x{color[2:4]}", 16), int(f"0x{color[4:6]}", 16)]

def setComponents(componentsFileName):
    #ouvrir le fichier contenant les composants
    file = open(componentsFileName)
    componentsDict = eval(file.read())
    file.close()

    #pour chaque nom de composant parmis ceux dans le fichier
    for componentName in componentsDict.keys():
        #pour chaque élément contenu dans le nom du composant
        for componentClassName in componentsDict[componentName].keys():
            try:
                #vérifie si l'élément est un composant
                eval(componentClassName)
            except:
                #test si l'élément est une div
                if componentClassName in componentsDict.keys():
                    divs[componentName] = componentsDict[componentName]
                #ou un groupe de paramètres
                else:
                    settingsGroups[componentName] = componentsDict[componentName]
            else:
                components[componentName] = createComponent(componentClassName, componentsDict[componentName][componentClassName])

def createComponent(name, settings):
    return eval(f"{name}({settings})")

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
                self.components[componentName].setEnvironnement(size)

    def globalSetup(self, componentClassName, additionalSettings):
        if self.settings["settings"]:
            #si le paramêtre 'setting' est un groupe de paramêtres, on ajoute chacun des paramêtres aux paramêtres du composant
            if type(self.settings["settings"]) == str:
                for key in settingsGroups[self.settings["settings"]].keys():
                    try:
                        self.settings[key]
                    except:
                        self.settings[key] = settingsGroups[self.settings["settings"]][key]

            #si le paramêtre 'setting' est une liste de groupe de paramêtre, on ajoute chacun des paramêtres de chaque groupe au paramêtres du composant
            elif type(self.settings["settings"]) == list:
                for settingsGroup in self.settings["settings"]:
                    for key in settingsGroups[settingsGroup].keys():
                        try:
                            self.settings[key]
                        except:
                            self.settings[key] = settingsGroups[self.settings["settings"]][key]

            del self.settings["settings"]

            for setting in additionalSettings.keys():
                self.settings[setting] = additionalSettings[setting]

        #pour tout les paramêtres requis mais vides, on applique la valeur par défaut
        for setting in requirements[componentClassName]:
            if not setting in self.settings.keys():
                self.settings[setting] = default[setting]

    def setEnvironnement(self, size):
        self.containerSize = size
        self.containerPosition = [0, 0]

    def show(self):
        for componentName in self.components.keys():
            self.components[componentName].showComponent(self.screen)

class Button(Page):
    def __init__(self, settings):
        self.settings = settings
        self.widgets = {}

    def setup(self, additionalSettings = {}):
        self.globalSetup("Button", additionalSettings)

    def showComponent(self, screen):
        position = convertPosition(self.settings["position"].copy(), self.containerPosition, self.containerSize)
        size = convertSize(self.settings["size"].copy(), self.containerSize)

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
