import os
import json
import yaml
import time
import datetime
import subprocess
from pathlib import Path
import git

def get_last_build_id():
    """Get the last build ID from data.json if it exists, otherwise return 0."""
    try:
        if os.path.exists('data.json'):
            with open('data.json', 'r') as f:
                data = json.load(f)
                return data['header']['info']['build_id']
    except Exception as e:
        print(f"Error reading last build ID: {e}")
    return 0

def increment_build_id():
    """Get the last build ID and increment it by 1."""
    last_id = get_last_build_id()
    return last_id + 1

def get_git_branch():
    """Get current git branch name by searching parent directories for .git folder."""
    current_path = os.getcwd()
    while current_path != '/':
        try:
            repo = git.Repo(current_path, search_parent_directories=True)
            return repo.active_branch.name
        except:
            current_path = os.path.dirname(current_path)
    return "unknown"

def get_file_tree(start_path):
    """Generate file tree structure directly using subprocess."""
    try:
        result = []
        # Run tree command and capture output
        process = subprocess.run(
            ['tree', '--noreport', '-h', '-F', '-I', 'node_modules'],
            capture_output=True,
            text=True,
            cwd=start_path
        )
        
        if process.returncode == 0:
            # Process the output to match desired format
            lines = process.stdout.strip().split('\n')
            for line in lines:
                # Remove any color codes if present
                line = line.strip()
                if line:
                    result.append(line)
            return result
        else:
            return ["root/"]
            
    except Exception as e:
        print(f"Error generating file tree: {e}")
        return ["root/"]



def get_directory_stats(start_path, max_depth, allowed_extensions, ignore_patterns, log_dir):
    """Calculate directory statistics with detailed logging."""
    # Ensure logs directory exists
    ensure_directory_exists(log_dir)
    
    # Setup stats logging
    log_file = os.path.join(log_dir, 'stats_log.txt')
    with open(log_file, 'w') as log:
        def log_write(message):
            log.write(f"{message}\n")
            print(message)  # Also print to console

        total_files = 0
        total_folders = 0
        total_size = 0
        last_modified = None        
        log_write("\n=== INITIAL PARAMETERS ===")
        log_write(f"Start path: {start_path}")
        log_write(f"Max depth: {max_depth}")
        log_write(f"Allowed extensions: {allowed_extensions}")
        log_write(f"Ignore patterns: {ignore_patterns}")

        # Normalize allowed extensions
        allowed_extensions = [ext.lower().lstrip('.') for ext in allowed_extensions]
        log_write(f"Normalized allowed extensions: {allowed_extensions}")
        
        def should_ignore(name, patterns):
            """Check if a file or directory name should be ignored based on patterns."""
            for pattern in patterns:
                if pattern.startswith('*') and pattern.endswith('*'):
                    # Pattern like "*hidden*" - check if substring exists
                    if pattern[1:-1] in name:
                        return True
                elif pattern.startswith('*'):
                    # Pattern like "*hidden" - check suffix
                    if name.endswith(pattern[1:]):
                        return True
                elif pattern.endswith('*'):
                    # Pattern like ".*" or "_*" - check prefix
                    if name.startswith(pattern[:-1]):
                        return True
                else:
                    # Exact match
                    if name == pattern:
                        return True
            return False
        
        log_write("\n=== STARTING DIRECTORY SCAN ===")
        
        for root, dirs, files in os.walk(start_path):
            # Calculate depth
            rel_path = os.path.relpath(root, start_path)
            current_depth = len(Path(rel_path).parts) if rel_path != '.' else 0
            
            log_write(f"\n--- Processing Directory ---")
            log_write(f"Current directory: {root}")
            log_write(f"Depth: {current_depth}")
            log_write(f"Original dirs found: {dirs}")
            log_write(f"Original files found: {files}")

            # Check depth
            if current_depth > max_depth:
                log_write(f"Skipping - exceeded max depth {max_depth}")
                dirs.clear()
                continue

            # Process directories
            original_dirs = dirs.copy()
            dirs[:] = [d for d in dirs if not should_ignore(d, ignore_patterns)]
            filtered_dirs = set(original_dirs) - set(dirs)
            
            log_write("\n-- Directory Processing --")
            log_write(f"Filtered out directories: {filtered_dirs}")
            log_write(f"Remaining directories: {dirs}")
            
            total_folders += len(dirs)
            log_write(f"Added {len(dirs)} to folder count. New total: {total_folders}")

            # Process files
            log_write("\n-- File Processing --")
            for file in files:
                log_write(f"\nChecking file: {file}")
                
                # Check ignore patterns
                if should_ignore(file, ignore_patterns):
                    log_write(f"Skipping - matches ignore pattern: {file}")
                    continue

                # Check extension
                ext = os.path.splitext(file)[1].lower().lstrip('.')
                log_write(f"File extension: {ext}")
                log_write(f"Checking against allowed extensions: {allowed_extensions}")
                
                if ext in allowed_extensions:
                    file_path = os.path.join(root, file)
                    try:
                        file_stat = os.stat(file_path)
                        file_size = file_stat.st_size
                        total_files += 1
                        total_size += file_size
                        
                        if last_modified is None or file_stat.st_mtime > last_modified:
                            last_modified = file_stat.st_mtime
                        
                        log_write(f"COUNTED: {file}")
                        log_write(f"Size: {file_size} bytes")
                        log_write(f"Running totals - Files: {total_files}, Size: {total_size}")
                    except OSError as e:
                        log_write(f"Error processing file {file}: {e}")
                        continue
                else:
                    log_write(f"Skipping - extension not allowed: {file}")

        log_write("\n=== FINAL STATISTICS ===")
        log_write(f"Total files: {total_files}")
        log_write(f"Total folders: {total_folders}")
        log_write(f"Total size: {total_size}")
        log_write(f"Last modified: {time.strftime('%H_%M_%S', time.localtime(last_modified)) if last_modified else '00_00_00'}")

        return {
            "total_files": total_files,
            "total_folders": total_folders,
            "total_size": total_size,
            "last_modified": time.strftime('%H_%M_%S', time.localtime(last_modified)) if last_modified else "00_00_00"
        }



def get_formatted_datetime():
    """Get current date and time in separate formats."""
    now = datetime.datetime.now()
    return {
        "date": now.strftime("%Y_%m_%d"),
        "timestamp": now.strftime("%H_%M_%S")
    }

def read_config():
    """Read and parse config.yml file."""
    try:
        with open("config.yml", 'r') as file:
            config_data = yaml.safe_load(file)
            print("Successfully loaded config.yml")
            return config_data
    except Exception as e:
        print(f"Error reading config.yml: {e}")
        return None



def ensure_directory_exists(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def read_config(config_path):
    """Read and parse config file from specified path."""
    try:
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)
            print(f"Successfully loaded {config_path}")
            return config_data
    except Exception as e:
        print(f"Error reading {config_path}: {e}")
        return None

def write_file_structure(data, config):
    """Write the file structure data to JSON file specified in config."""
    filename = config["files"].get("filename", "data.json")
    # Use root path from config
    root_path = config["paths"]["root"]
    full_path = os.path.join(root_path, filename)
    
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent='\t', ensure_ascii=False)
        print(f"Successfully generated {full_path}")
    except Exception as e:
        print(f"Error writing to {full_path}: {e}")





def main():
    # Get initial config path from command line or use default
    initial_config_path = "config.yml"
    
    # Read initial configuration to get actual paths
    initial_config = read_config(initial_config_path)
    if not initial_config:
        return

    # Get actual config path and other directories
    root_path = initial_config["paths"]["root"]
    config_path = os.path.join(root_path, initial_config["paths"]["config"])
    logs_path = os.path.join(root_path, initial_config["paths"]["logs"])
    
    # Ensure logs directory exists
    ensure_directory_exists(logs_path)
    
    # Read full configuration from actual config path
    config_data = read_config(config_path)
    if not config_data:
        return
    
    # Get new build ID and other data
    build_id = increment_build_id()
    version = config_data.get("info", {}).get("version", "0.0.1")
    datetime_info = get_formatted_datetime()
    
    # Build header structure
    header = {
        "info": {
            "version": version,
            "build_id": build_id,
            "date": datetime_info['date'],
            "timestamp": datetime_info['timestamp']
        },
        "git": {
            "git_branch": get_git_branch()
        },
        "stats": get_directory_stats(
            root_path,  # Use root path as start path
            config_data["files"]["max_depth"],
            config_data["files"]["allowed_extensions"],
            config_data["files"]["ignore_patterns"],
            logs_path  # Pass logs path to stats function
        ),
        "config": {
            "paths": config_data["paths"],
            "files": config_data["files"],
            "display": config_data["display"]
        },
        "media": config_data["media"],
        "dir_tree": config_data["dir_tree"],
        "html_content": config_data["html_content"],
        "threejs_scene": config_data["threejs_scene"],
        "tree": get_file_tree(root_path)  # Use root path for tree
    }

    # Create and write final structure
    final_data = {
        "header": header,
        "structure": {}
    }
    write_file_structure(final_data, config_data)

if __name__ == "__main__":
    main()
