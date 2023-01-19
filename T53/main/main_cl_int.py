import os
import json
import argparse
import pandas as pd
import numpy as np
import ActionFinderModule as afm
import tools5dot2
import main_cluster_maker as mcm
from scen_gen import update_table
import config as cfg

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

class T53Tool():
	def __init__(
            self,
            argsParsed
    ):
		self.jsonConfig = argsParsed
		self.year = self.jsonConfig["nScenarios"]

	def getConfig(self):
		return self.jsonConfig

	def generate_results(self):
		print("Generating Result (First Part)")
		filePath = self.jsonConfig["path"]
		with open(filePath, 'r') as f:
			self.config = json.load(f)
		self.assets = self.jsonConfig["assetsName"]

		for config in self.config:
			path_ref_file = config["path"]
			path_conf_file= "../files/ConfigurationFile.csv"
			years = self.year
			var_list = config["variables"]
			var_time = ""
			var_name = config["index"]

			try:
				update_table(path_ref_file,path_conf_file, years,var_list,var_time,var_name, self.assets)
			except IndexError:
				return

		# wp52_output_path = os.path.join("../Result/Result from tools5.2", self.assets)
		wp52_output_path = os.path.join(cfg.output_dir_from_config_1, "Result_from_T52")
		os.makedirs(wp52_output_path, exist_ok=True)


		print(tools5dot2.tool5dot2_calculate(self.config, 
                                             file_name=self.assets,
                                             years=self.year, 
                                             save_results_to=wp52_output_path))

class T52Tool():
	def __init__(
            self,
            argsParsed
    ):
		self.jsonConfig = argsParsed

	def generate_results(self):
		print("Generating Result (T52 Tool)")
		self.folderPath = self.jsonConfig["input_dir"]
		mcm.input_data_2(self.folderPath)

class ActionsTool():
	def __init__(
            self,
            argsParsed
    ):
		self.jsonConfig = argsParsed
	
	def generate_result(self):
		print("Generating Result (Actions Tool)")
		
		self.folderPath = self.jsonConfig["input_dir"]
        
		self.afmodule = afm.ActionFinder(
			indicator_folder=self.folderPath,
			qtable_filename="../files/Q_learning_approach.xlsx")
		self.afmodule.calculateHML()
		self.afmodule.calculateAllPossibleAction()
		self.afmodule.findingAction()

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

	cfg.output_dir_from_config_1 = jsonParsed['firstConfig']['output_dir']
	cfg.output_dir_from_config_2 = jsonParsed['t52Config']['output_dir']
	cfg.output_dir_from_config_3 = jsonParsed['actionsConfig']['output_dir']
	print(f'Output dir 1: {cfg.output_dir_from_config_1}')
	print(f'Output dir 2: {cfg.output_dir_from_config_2}')
	print(f'Output dir 3: {cfg.output_dir_from_config_3}')

	t53Tool = T53Tool(jsonParsed["firstConfig"])
	t53Tool.generate_results()

	t52Tool = T52Tool(jsonParsed["t52Config"])
	try:
		t52Tool.generate_results()
	except Exception as e:
		print(f"WARNING: {str(e)}")

	actionsTool = ActionsTool(jsonParsed["actionsConfig"])
	actionsTool.generate_result()

if __name__ == '__main__':
    main()