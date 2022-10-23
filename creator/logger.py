import sys

class Logger:
	def __init__(self, verbose=False):
		self.verbose=verbose
	
	def panic(self, msg):
		sys.stderr.write(f"CRITICAL ERROR : {msg}\n")
		sys.exit(1)
	
	def warning(self, msg):
		sys.stdout.write(f"WARNING : {msg}\n")

	def log(self, msg):
		if self.verbose:
			sys.stdout.write(f"{msg}\n")