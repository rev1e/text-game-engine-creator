class ParserError(Exception):
	def __init__(self, file, message):
		if file:
			super().__init__(f"{file} : {message}")
		else:
			super().__init__(message)

def parse(rooms, metadata, logger):
	logger.log("Stage 2 - Creating Names Map")
	names = {}
	for i, name in enumerate(rooms.keys()):
		names[name] = i
	
	logger.log("Stage 3 - Changing Choices 'to' field")
	for (name, room) in rooms.items():
		if not "choices" in room:
			continue
		
		logger.log(f"changing {name}")

		for c in room["choices"]:
			if not c["to"] in names:
				raise ParserError(name+".toml", f"room {c['to']} doesn't exist")
			c["to"] = names[c["to"]]

	logger.log("Stage 5 - Creating output")

	metadata["entry"] = names[metadata["entry"]]

	return {
		"metadata": metadata,
		"rooms": list(rooms.values())
	}

