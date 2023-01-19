import sys
import shutil
from click import command

import xlrd
import pandas as pd
from openpyxl import load_workbook

import json
import argparse
import config

sys.path.append("..")
from chart.lib.main_condition_monitoring import *

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

class T512Tool():
	def __init__(
            self,
            argsParsed
    ):
		self.configs = argsParsed

	def getConfigs(self):
		return self.configs

	def generate_results(self):
		print("Generating Result")

		model_path = self.configs["modelpath1"]
		model_error_path = self.configs["modelpath2"]
		input_file_path = self.configs["filepath2"]

		current_var = self.configs["item1"]
		oil_temp_var = self.configs["item2"]
		winding_temp_var = self.configs["item3"]

		generate_prediction_dashboard(model_path, model_error_path, input_file_path, current_var, oil_temp_var,winding_temp_var)

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
	config.output_dir_from_config = jsonParsed['output_dir']
	app = T512Tool(jsonParsed)
	# print("updated configs: " + str(app.getConfigs()))
	app.generate_results()

if __name__ == '__main__':
    main()