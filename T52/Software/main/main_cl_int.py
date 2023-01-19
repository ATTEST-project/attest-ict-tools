import json
import argparse
import pandas as pd
from utils import *
from main_cluster_maker import *
import config
region_coordinates = {'asia': [34.0479, 100.6197], 'europe': [53.0000, 9.0000], 'africa': [9.1021, 18.2812], 'usa': [44.5000, -89.500]}

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

class T52Tool():
	def __init__(
            self,
            argsParsed
    ):
		self.configs = argsParsed

	def getConfigs(self):
		return self.configs

	def getOutputDir(self):
		return self.configs['output_dir']
	
	def performStep1(self):
		columnsList = []
		index_column = []
		for config in self.configs['mainConfig']:
			print(f"\nConfig: {config}")
			columns = []
			variablesLength = len(config['variables'])
			print(f"\nVariables length: {variablesLength}")
			for i in range(variablesLength):
				column = config['variables'][i]
				columns.append(column)
			print(f"\nColumns: {columns}")
			new_column_name = config['config']
			weights = config['weights']
			weights = list(map(float, weights))
			dataset = read_file1(config['path'], col_name = config['index'])
            
			print(f"\nDataset: {dataset}")
			index_column = dataset.index.values.tolist()
			print(f"\nIndex Column: {index_column}")
			data = sum(weights, dataset[columns])
			columnsList.append(pd.DataFrame(data, columns=[new_column_name]))

		final_df = pd.concat(columnsList, axis=1)
		final_df.insert(0, 'index', index_column)
		final_df.set_index('index', inplace=True)
		final_df['Total_Indicator'] = final_df.sum(axis=1)/len(final_df.columns)

		return final_df.round(decimals=3)

	def generateResults(self):
		print("Generating Result")

		output = self.performStep1()

		# if 'coordinatesConfig' in self.configs and self.configs['coordinatesConfig']['coordinatesFilePath'] != "":
		if 'coordinatesConfig' in self.configs and self.configs['coordinatesConfig'] != None and self.configs['coordinatesConfig']['coordinatesFilePath'] != "":
			coordinateConfig = self.configs['coordinatesConfig']
			print(f"\nCoordinate Config: {coordinateConfig}")
			coordinatesFilePath = coordinateConfig['coordinatesFilePath']
			coordinatesIdentifier = coordinateConfig['coordinatesIdentifier']
			latColumn = coordinateConfig['latColumn']
			longColumn = coordinateConfig['longColumn']
			regionCB = coordinateConfig['regionCB']

			coordinatesFile = pd.read_csv(coordinatesFilePath, index_col=coordinatesIdentifier)
			coordinatesFile = coordinatesFile[[latColumn, longColumn]]

			final_df = pd.merge(output, coordinatesFile, left_index=True, right_index=True)
			final_df.rename({latColumn: 'lat', longColumn: 'long'}, axis=1, inplace=True)
			final_df = final_df.round(decimals=3)

			create_map(final_df, region_coordinates[regionCB.lower()], output_dir=config.output_dir_from_config)
		else:
			final_df = output
			final_df['lat'] = ""
			final_df['long'] = ""

		# print(f"\nFinal_df: {final_df}")

		final_df.to_csv(config.output_dir_from_config + 'final.csv', index=True)
		print("\nFile saved to: {'final.csv'}")

		# output_dir_from_config = self.configs['output_dir']
		# output = pd.read_csv('final.csv', index_col=0)
		input_data(final_df[final_df.columns[:-2]]) # removing lat long columns

		print("\nResults generated.")

def sum(weight, dataset):
	weights = pd.Series(weight, index=dataset.columns)
	new_data = dataset * weights
	new_data = new_data.sum(axis=1)
	return new_data

def read_file1(path, col_name):
	csv_header_1 = pd.read_csv(path, sep=";")
	csv_header_2 = pd.read_csv(path)
	df = pd.read_csv(path, index_col=col_name, sep=";") if len(csv_header_1.columns) >= len(csv_header_2.columns) else pd.read_csv(path, index_col=col_name)
	
	df= df.select_dtypes(include=np.number)
	NormalizeData= lambda x: (x- x.min(axis=0)) / (x.max(axis=0) - x.min(axis=0))
	data = df.apply(NormalizeData)
	return data

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
	app = T52Tool(jsonParsed)
	config.output_dir_from_config = jsonParsed['output_dir']
	# print(f"Original Config: {app.getConfigs()}\n")
	app.generateResults()

if __name__ == '__main__':
    main()