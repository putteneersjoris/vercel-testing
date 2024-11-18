import os
import yaml

def get_config_value(config, *keys, default=None):
    current = config
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key, default)
        else:
            return default
    return current

def load_config():
    config_path = "./scripts/config.yml"
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def get_output_path(config):
    filename = get_config_value(config, 'files', 'filename', default='data.json')
    scripts_path = get_config_value(config, 'paths', 'scripts', default='./scripts')
    return os.path.join(scripts_path, filename)
