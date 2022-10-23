class ParserError(Exception):
	def __init__(self, file, message):
		if file:
			super().__init__(f"{file} : {message}")
		else:
			super().__init__(message)

def parse(rooms, images, metadata, logger):
	logger.log("Stage 2 - Creating Names Map")
	names = {}
	for i, name in enumerate(rooms.keys()):
		names[name] = i

	if not images is None:
		image_names = {}
		for i, name in enumerate(images.keys()):
			image_names[name] = i
	
	logger.log("Stage 3 - Changing Fields")
	for (name, room) in rooms.items():
		if not "choices" in room:
			continue
		
		logger.log(f"changing choices {name}")

		for c in room["choices"]:
			if not c["to"] in names:
				raise ParserError(name+".toml", f"room {c['to']} doesn't exist")
			c["to"] = names[c["to"]]

	# image name change
	for (name, room) in rooms.items():
		if "image" not in room:
			continue
		
		logger.log(f"changing image {name}")

		if images is None or room["image"] not in image_names:
			raise ParserError(name, "image not found")

		room["image"] = image_names[room["image"]];

	logger.log("Stage 5 - Creating output")

	metadata["entry"] = names[metadata["entry"]]

	output = {
		"metadata": metadata,
		"rooms": list(rooms.values()),
	}

	if not images is None:
		output["images"] = list(images.values())

	return output

