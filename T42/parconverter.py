# WP6 
# convert a json into a properties file that can be read from the launch script to set the input parameters

import sys
import json

def json_to_properties(json_file_path, properties_file_path):
    # Load the JSON data from file
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
		
	# Check if 'parameters' key exists
    if 'parameters' not in json_data:
        print("'parameters' key not found in JSON data.")
        sys.exit(-1)
        return	

    # Write the properties data to file
    with open(properties_file_path, 'w') as properties_file:
        for key, value in json_data['parameters'].items():
            properties_file.write('{}={}\n'.format(key, value))

    print('Successfully converted {} to {}'.format(json_file_path, properties_file_path))

if len(sys.argv) < 2:
    print("Usage: python parconverter.py <json_file>")
    sys.exit(1)


json_file_path = sys.argv[1]
properties_file_path = sys.argv[2]

# Convert the JSON file to a properties file
json_to_properties(json_file_path, properties_file_path)

