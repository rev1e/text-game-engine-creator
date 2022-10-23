#!/usr/bin/env python3
import argparse
import os, sys
import json

from creator.logger import Logger
from creator.parser import ParserError
import creator

# parse arguments
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("--force", "-f", help="delete output file if it exists", action="store_true")
arg_parser.add_argument("--verbose", "-v", help="show more information", action="store_true")

arg_parser.add_argument("source", help="directory where source files are located")
arg_parser.add_argument("output", help="output file")

args = arg_parser.parse_args()

logger = Logger(args.verbose)

# check source directory
try:
	creator.check_source_directory(args.source)
except Exception as err:
	logger.panic(err)

# check output file
if os.path.isfile(args.output) and not args.force:
	logger.panic("output file exists")
if not args.output.endswith(".tg"):
	logger.warning("it is recommended that output file ends with .tg extension")

# parse files
try:
	output = creator.parse_source_directory(args.source, logger)
except ParserError as e:
	logger.panic(e)

logger.log("Stage 6 - Creating And Writing JSON")
output = json.dumps(output, separators=(',', ':'))

with open(args.output, mode="wt", encoding="utf-8") as f:
    f.write(output)