import os, json

def importConfigFiles():
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

	return defaults, requirements, aliases
			
"""def defineElements(elementsFileName):
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
			settingsGroups[element] = elements[element]"""