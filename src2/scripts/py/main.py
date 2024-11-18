import json
from config_utils import load_config, get_output_path
from header_utils import create_header
from structure_utils import create_structure
from image_utils import process_images
from logger import setup_logging

def write_json(data, config):
    output_path = get_output_path(config)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    log_file = setup_logging()
    config = load_config()
    
    # Process images before creating structure
    processed_paths = process_images(config, log_file)
    
    # Add processed paths to config for structure creation
    config['processed_paths'] = processed_paths
    
    header = create_header(config, log_file)
    structure = create_structure(config, log_file)
    
    data = {
        "header": header["header"],
        "structure": structure
    }
    
    write_json(data, config)

if __name__ == "__main__":
    main()
