#!/usr/bin/env python3
import argparse
import os
import sys
import toml
import json
import io

def panic(msg):
    sys.stderr.write(f"{msg}\n")
    sys.exit(1)

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("source", help="directory where source files are located")
arg_parser.add_argument("output", help="output file")
args = arg_parser.parse_args()
rooms_directory = os.path.join(args.source, "rooms")

if not os.path.isdir(args.source):
    panic("source directory doesnt exist")

if not os.path.isdir(rooms_directory):
    panic("rooms directory doesnt exist")

if os.path.exists(args.output):
    panic("output file exists")

files = os.listdir(args.source)
if not "metadata.toml" in files:
    panic("no metadata.toml file")

metadata = toml.load(os.path.join(args.source, "metadata.toml"))

names = {}
rooms = []

# stage 1 - load content
for file in os.listdir(rooms_directory):
    print("parsing", file)
    if not file.endswith(".toml"):
        continue
    
    # TODO error handeling
    room = toml.load(os.path.join(rooms_directory, file))

    # change name of choices list
    room["choices"] = room.pop("choice")
    
    room["text"] = room["text"].strip()
    for c in room["choices"]:
        c["text"] = c["text"].strip()

    # remove .toml
    filename = file[:-5]

    rooms.append(room)
    names[filename] = len(rooms) - 1

# stage 2 - change names
for room in rooms:
    for choice in room["choices"]:
        # TODO error handling
        choice["to"] = names[choice["to"]]

content = { "entry": names[metadata["entry"]], "id": metadata["id"], "rooms": rooms }
content = json.dumps(content, separators=(',', ':'))

with open(args.output, mode="wt", encoding="utf-8") as f:
    f.write(content)
