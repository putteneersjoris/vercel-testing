import os
import yaml
import json
import datetime
import subprocess
from pathlib import Path

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

def get_last_build_id(config):
    try:
        output_path = get_output_path(config)
        if os.path.exists(output_path):
            with open(output_path, 'r') as f:
                data = json.load(f)
                return data['header']['info']['build_id']
    except Exception as e:
        print(f"Error reading build ID: {e}")
    return 0

def get_directory_tree(root_path):
    try:
        result = []
        process = subprocess.run(
            ['tree', '--noreport', '-h', '-F', '-I', 'node_modules'],
            capture_output=True,
            text=True,
            cwd=root_path
        )
        
        if process.returncode == 0:
            return process.stdout.strip().split('\n')
        else:
            return ["root/"]
            
    except Exception as e:
        print(f"Error generating tree: {e}")
        return ["root/"]

def setup_logging():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = "./scripts/logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"dir_scan_{timestamp}.log")
    return log_file

def log_message(file, message):
    print(message)
    with open(file, 'a') as f:
        f.write(f"{message}\n")

def get_directory_stats(config, log_file):
    root_path = get_config_value(config, 'paths', 'root', default='./')
    max_depth = get_config_value(config, 'files', 'max_depth', default=5)
    allowed_extensions = get_config_value(config, 'files', 'allowed_extensions', default=[])
    ignore_patterns = get_config_value(config, 'files', 'ignore_patterns', default=[])
    
    log_message(log_file, "\n=== Directory Scan Started ===")
    log_message(log_file, f"Root path: {root_path}")
    log_message(log_file, f"Max depth: {max_depth}")
    log_message(log_file, f"Allowed extensions: {allowed_extensions}")
    log_message(log_file, f"Ignore patterns: {ignore_patterns}")
    
    total_files = 0
    total_folders = 0
    total_size = 0
    
    def should_ignore(name, patterns):
        for pattern in patterns:
            if pattern.startswith('*') and pattern.endswith('*'):
                if pattern[1:-1] in name:
                    return True
            elif pattern.startswith('*'):
                if name.endswith(pattern[1:]):
                    return True
            elif pattern.endswith('*'):
                if name.startswith(pattern[:-1]):
                    return True
            elif name == pattern:
                return True
        return False

    for root, dirs, files in os.walk(root_path):
        depth = root[len(root_path):].count(os.sep)
        log_message(log_file, f"\nProcessing directory: {root}")
        log_message(log_file, f"Current depth: {depth}")
        
        if depth > max_depth:
            log_message(log_file, f"Skipping - exceeded max depth {max_depth}")
            dirs.clear()
            continue
            
        original_dirs = dirs.copy()
        dirs[:] = [d for d in dirs if not should_ignore(d, ignore_patterns)]
        filtered_dirs = set(original_dirs) - set(dirs)
        
        if filtered_dirs:
            log_message(log_file, f"Filtered directories: {filtered_dirs}")
        
        total_folders += len(dirs)
        log_message(log_file, f"Counted folders: {len(dirs)}")
        
        for file in files:
            if should_ignore(file, ignore_patterns):
                log_message(log_file, f"Ignored file: {file}")
                continue
                
            ext = os.path.splitext(file)[1].lower().lstrip('.')
            if ext in allowed_extensions:
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    total_files += 1
                    total_size += size
                    log_message(log_file, f"Added file: {file} ({size} bytes)")
                except OSError as e:
                    log_message(log_file, f"Error processing file {file}: {e}")
                    continue

    log_message(log_file, "\n=== Final Statistics ===")
    log_message(log_file, f"Total files: {total_files}")
    log_message(log_file, f"Total folders: {total_folders}")
    log_message(log_file, f"Total size: {total_size} bytes")

    return {
        "total_files": total_files,
        "total_folders": total_folders,
        "total_size": total_size
    }

def create_header(config):
    log_file = setup_logging()
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d")
    time = datetime.datetime.now().strftime("%H_%M_%S")
    build_id = get_last_build_id(config) + 1
    root_path = get_config_value(config, 'paths', 'root', default='./')
    
    header = {
        "header": {
            "info": {
                "version": get_config_value(config, 'info', 'version', default='0.0.1'),
                "build_id": build_id,
                "timestamp": timestamp,
                "git_branch": "main"
            },
            "stats": get_directory_stats(config, log_file),
            "tree": get_directory_tree(root_path),
            "config": config,
            "media": get_config_value(config, 'media', default={}),
            "dir_tree": get_config_value(config, 'dir_tree', default={}),
            "html_content": get_config_value(config, 'html_content', default={}),
            "threejs_scene": get_config_value(config, 'threejs_scene', default={})
        }
    }
    return header



def write_json(data, config):
    output_path = get_output_path(config)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    config = load_config()
    header = create_header(config)
    write_json(header, config)

if __name__ == "__main__":
    main()
