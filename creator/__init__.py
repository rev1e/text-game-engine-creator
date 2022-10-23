import os
import toml
import base64

from .parser import ParserError, parse

def check_source_directory(dir):
	if not os.path.isdir(dir):
		raise Exception("source directory doesn't exist")
	# metadata must exist
	if not os.path.isfile(os.path.join(dir, "metadata.toml")):
		raise Exception("metadata.toml doesn't exist")
	# rooms must exist
	if not os.path.isdir(os.path.join(dir, "rooms")):
		raise Exception("rooms directory doesnt' exist")

def validate_metadata(metadata):
	if not "entry" in metadata:
		raise Exception("no 'entry'")
	if not "id" in metadata:
		raise Exception("no 'id'")

def validate_room(room):
	if not "text" in room:
		raise Exception("no 'text'")
	
	if "choice" in room:
		for c in room["choice"]:
			if "text" not in c:
				raise Exception("no 'text' in choice")
			if "to" not in c:
				raise Exception("no 'to' in choice")

def parse_source_directory(dir, logger):
	logger.log("Stage 1 - Loading Rooms")

	logger.log(f"Loading metadata.toml")

	try:
		metadata = toml.load(os.path.join(dir, "metadata.toml"))
	except toml.decoder.TomlDecodeError as err:
		raise ParserError("metadata.toml", err)

	try:
		validate_metadata(metadata)
	except Exception as err:
		raise ParserError("metadata.toml", err)

	files = os.listdir(os.path.join(dir, "rooms"))

	if metadata["entry"] + ".toml" not in files:
		raise ParserError("metadata.toml", "entry doesn't exist")

	rooms = {}

	for file in files:
		if not file.endswith('.toml'):
			continue
		logger.log(f"Loading {file}")
		try:
			room = toml.load(os.path.join(dir, "rooms", file))
		except toml.decoder.TomlDecodeError as err:
			raise ParserError(file, err)
		
		try:
			validate_room(room)
		except Exception as err:
			raise ParserError(file, err)
		
		# change choice to choices
		if "choice" in room:
			room["choices"] = room.pop("choice")

		rooms[file.replace(".toml", "")] = room

	images = None
	if os.path.isdir(os.path.join(dir, "images")):
		images = {}
		logger.log("Stage 1.5 - Loading Images")
		files = os.listdir(os.path.join(dir, "images"))
		for file in files:
			# only support png images for now
			if not file.endswith(".png"):
				continue
			image_path = os.path.join(dir, "images", file)
			with open(image_path, "rb") as f:
				images[file] = base64.b64encode(f.read()).decode("utf-8")
	
	return parse(rooms, images, metadata, logger)
