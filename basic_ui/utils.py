def adder(number):
	def add(value):
		return number + value
	return add

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

def convertColor(color, aliases):
	"""convertColor : fonction permettant de convertir une color depuis le format utilisé dans la page json en color RVB"""
	if color in aliases.keys():
		color = aliases[color]

	if len(color) == 1:
		color = color * 6
	elif len(color) == 3:
		color = color[0] * 2 + color[1] * 2 + color[2] * 2

	return [int(f"0x{color[0:2]}", 16), int(f"0x{color[2:4]}", 16), int(f"0x{color[4:6]}", 16)]

class WindowSize:
	def __init__(self, size):
		self.size = size

	def convert(self):
		return self.size.copy()
	
class WindowPosition:
	def __init__(self, position):
		self.position = position

	def convert(self):
		return self.position.copy()

class Size:
	def __init__(self, component):
		self.size = component.settings["size"]
		self.containerSize = component.container.size
		print(self.containerSize.convert())

	def convert(self, autoSize = []):
		if self.size != "auto":
			size = self.size.copy()
			
			for i in range(2):
				if size[i].endswith("%"):
					size[i] = self.containerSize.convert()[i] / 100 * int(size[i][0:-1])
					
				elif size[i].endswith("px"):
					size[i] = int(size[i][0:-2])

			if autoSize[0] > size[0]:
				size[0] = autoSize[0]

			if autoSize[1] > size[1]:
				size[1] = autoSize[1]

		else:
			size = autoSize

		return size

class Position:
	def __init__(self, component):
		self.position = component.settings["position"]
		self.containerPosition = component.container.position
		self.containerSize = component.container.size

	def convert(self):
		position = self.position.copy()

		for i in range(2):
			if position[i].endswith("%"):
				position[i] = (self.containerPosition.convert()[i] + self.containerSize.convert()[i] / 100) * int(position[i][0:-1])
			elif position[i].endswith("px"):
				position[i] = self.containerPosition.convert()[i] + int(position[i][0:-2])

		return position