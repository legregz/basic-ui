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