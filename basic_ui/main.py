from . import button
from . import label
from . import section
from . import window
from . import functions

default, requirements, aliases = functions.importConfigFiles()

def Label(settings):
	return label.Label(settings, requirements["Label"])

def Button(settings):
	return button.Button(settings, requirements["Button"])

def Section(elements, settings):
	return section.Section(elements, settings, requirements["Section"])