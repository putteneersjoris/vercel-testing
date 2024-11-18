import os
import json
import datetime
import subprocess
from config_utils import get_config_value
from logger import log_message


def get_directory_tree(root_path, config):
    try:
        ignore_patterns = get_config_value(config, 'files', 'ignore_patterns', default=[])
        # Convert ignore patterns to tree-compatible format
        ignore_str = '|'.join(p.replace('*', '') for p in ignore_patterns)
        
        cmd = ['tree', '--noreport', '-F', '-I', f"node_modules|{ignore_str}"]
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=root_path
        )
        return process.stdout.strip().split('\n') if process.returncode == 0 else ["root/"]
    except Exception as e:
        print(f"Error generating tree: {e}")
        return ["root/"]

#
#def get_directory_tree(root_path):
#    try:
#        process = subprocess.run(
#            ['tree', '--noreport', '-h', '-F', '-I', 'node_modules'],
#            capture_output=True,
#            text=True,
#            cwd=root_path
#        )
#        return process.stdout.strip().split('\n') if process.returncode == 0 else ["root/"]
#    except Exception as e:
#        print(f"Error generating tree: {e}")
#        return ["root/"]

def get_last_build_id(config):
    try:
        output_path = get_config_value(config, 'paths', 'scripts', default='./scripts')
        filename = get_config_value(config, 'files', 'filename', default='data.json')
        file_path = os.path.join(output_path, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data['header']['info']['build_id']
    except Exception as e:
        print(f"Error reading build ID: {e}")
    return 0

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

    return {
        "total_files": total_files,
        "total_folders": total_folders,
        "total_size": total_size
    }

def create_header(config, log_file):
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d")
    time = datetime.datetime.now().strftime("%H_%M_%S")
    build_id = get_last_build_id(config) + 1
    root_path = get_config_value(config, 'paths', 'root', default='./')
    
    return {
        "header": {
            "info": {
                "version": get_config_value(config, 'info', 'version', default='0.0.1'),
                "build_id": build_id,
                "timestamp": timestamp,
                "git_branch": "main"
            },
            "stats": get_directory_stats(config, log_file),
            "tree": get_directory_tree(root_path,config),
            "config": config,
            "media": get_config_value(config, 'media', default={}),
            "dir_tree": get_config_value(config, 'dir_tree', default={}),
            "html_content": get_config_value(config, 'html_content', default={}),
            "threejs_scene": get_config_value(config, 'threejs_scene', default={})
        }
    }
