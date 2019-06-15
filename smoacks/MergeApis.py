# MergeApis.py - Utility for combining API specifications
import argparse
import glob
import os
import sys
import yaml

def merge_apis():
    # Define command line arguments for API merge
    parser = argparse.ArgumentParser(prog='smoacks-merge',
                                     description='SMOACKS API Merge Utility')
    parser.add_argument('-d', dest='dir', required=True, help='Directory containing specs to merge')
    parser.add_argument('-s', dest='output_spec', required=True, help='Output file name for merged specification')
    parser.add_argument('-t', dest='title', help='Title for resulting spec')
    opts = parser.parse_args()

    # Confirm that provided directory exists and is a directory
    if not os.path.isdir(opts.dir):
        sys.exit('{} is not a directory'.format(opts.dir))

    # Get list of specifications to merge
    spec_files = glob.glob(os.path.join(opts.dir, '*.yaml'))
    if len(spec_files) < 2:
        sys.exit('{} contains less than two specification files (*.yaml)'.format(opts.dir))

    # Confirm we can write to the output file
    out_spec = open(opts.output_spec, "w")
    if not out_spec:
        sys.exit('Cannot open {} for writing'.format(opts.output_spec))
    
    # Create the output dictionary that will hold the merged spec
    out_dict = {}

    # Iterate through specs and merge them into the output dictionary
    for spec_file in spec_files:
        try:
            spec_dict = yaml.load(open(spec_file), Loader=yaml.FullLoader)
        except:
            sys.exit('Error parsing {}, it probably is not YAML'.format(spec_file))

        # Update the spec before merging
        process_spec(spec_dict)

        # Merge in the spec to the output
        out_dict.update(spec_dict)

    # Set the title if it exists
    if (opts.title):
        out_dict['info']['title'] = opts.title

    # Write the merged output spec
    yaml.dump(out_dict, out_spec, default_flow_style=False)
    out_spec.close()

def process_spec(spec_dict):
    """Changes the paths for the spec"""

    # Get the root path for this spec from the URL attribute
    root_path = spec_dict['servers'][0]['url']

    # Remove the trailing specification path
    path_parts = root_path.split('/')
    path_prefix = path_parts.pop()

    # Save the new path
    new_path = path_parts.join('/')
    spec_dict['servers'][0]['url'] = new_path

    # Iterate through paths and update them 
    for path in spec_dict['paths']:
        path_data = spec_dict['paths'].pop(path)
        spec_dict['paths'][path_prefix + '/' + path] = path_data