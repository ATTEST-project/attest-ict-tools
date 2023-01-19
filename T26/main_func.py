from model_selector import *
import config

def main():
	energy = config.json_config['run_energy']
	secondary = config.json_config['run_secondary']
	tertiary = config.json_config['run_tertiary']
	
	model_selector(energy, secondary, tertiary)

if __name__ == '__main__':
    main()