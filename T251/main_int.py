import argparse
import json
import config
import main as t251main

class ArgParser():
	def __init__(
		self,
    ):
		self.initParser()

	def initParser(self):
		self.parser = argparse.ArgumentParser()
    
	def getParser(self):
		return self.parser

	def addArgument(self, command, type, default):
		self.parser.add_argument(
			"--" + str(command),  # name on the CLI - drop the `--` for positional/required parameters
			type=type, # str/int/float
			default=default,  # default if nothing is provided
		)

	def addArgumentList(self, command, nargs, type, default):
		self.parser.add_argument(
			"--" + str(command),  # name on the CLI - drop the `--` for positional/required parameters
			nargs=nargs,  # 0 or more values expected => creates a list
			type=type, # str/int/float
			default=default,  # default if nothing is provided
		)

def startArgsParser():
	args = ArgParser()
	args.addArgument("json", str, "[]")
	args.addArgument("json-file", str, "")
	parser = args.getParser()
	argsParsed = parser.parse_args()
	return argsParsed

def main():
	argsParsed = startArgsParser()
	jsonFile = open(argsParsed.json_file)
	jsonParsed = json.load(jsonFile)
	# print("\nJSON Parsed: " + str(jsonParsed))
	config.input_network_path = jsonParsed['input_network_path']
	config.input_resources_path = jsonParsed['input_resources_path']
	config.input_other_path = jsonParsed['input_other_path']
	config.output_dir = jsonParsed['output_dir']

	t251main.main()

if __name__ == '__main__':
    main()