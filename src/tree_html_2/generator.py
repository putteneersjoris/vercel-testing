import os
import json
import yaml
import time
import datetime
import subprocess
from pathlib import Path
import git

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
        # Get the parent directory of start_path
        parent_dir = os.path.dirname(start_path)
        
        # Run tree command
        result = subprocess.run(
            ['tree', parent_dir, '-F', '--noreport'],
            capture_output=True,
            text=True
        )
        
        # Split the output into lines and filter
        tree_lines = result.stdout.split('\n')
        # Remove empty lines and convert to the required format
        tree_lines = [line for line in tree_lines if line.strip()]
        
        return tree_lines
    except Exception as e:
        print(f"Error generating file tree: {e}")
        return ["root/"]

def get_directory_stats(root_path, max_depth, allowed_extensions, ignore_patterns):
    """Calculate directory statistics."""
    total_projects = 0
    total_files = 0
    total_folders = 0
    total_size = 0
    last_modified = None

    # Get the parent directory path
    parent_dir = os.path.dirname(root_path)

    for root, dirs, files in os.walk(parent_dir):
        level = root.replace(parent_dir, '').count(os.sep)
        if level > max_depth:
            continue

        # Skip ignored patterns
        dirs[:] = [d for d in dirs if not any(pattern.replace('*', '') in d for pattern in ignore_patterns)]
        files = [f for f in files if not any(pattern.replace('*', '') in f for pattern in ignore_patterns)]

        total_folders += len(dirs)
        
        for f in files:
            if any(f.endswith(ext) for ext in allowed_extensions):
                file_path = os.path.join(root, f)
                total_files += 1
                
                try:
                    file_size = os.path.getsize(file_path)
                    total_size += file_size
                    
                    mtime = os.path.getmtime(file_path)
                    if last_modified is None or mtime > last_modified:
                        last_modified = mtime
                except OSError:
                    continue

        # Count directories with specific project indicators as projects
        if any(indicator in files for indicator in ['package.json', 'setup.py', 'config.yml']):
            total_projects += 1

    return {
        "total_projects": total_projects,
        "total_files": total_files,
        "total_folders": total_folders,
        "total_size": total_size,
        "last_modified": time.strftime("%H_%M_%S", time.localtime(last_modified)) if last_modified else "00_00_00"
    }

def main():
    current_dir = os.getcwd()
    data_file = Path("data.json")
    
    # Read config.yml
    try:
        with open("config.yml", 'r') as file:
            config_data = yaml.safe_load(file)
    except Exception as e:
        print(f"Error reading config.yml: {e}")
        return

    # Initialize header structure
    header = {
        "info": {
            "version": "0.0.1",
            "build_id": 23,  # Hardcoded as specified
            "timestamp": datetime.datetime.now().strftime("%Y_%m_%d")
        },
        "git": {
            "git_branch": get_git_branch()
        },
        "config": config_data,
    }

    # Generate stats
    stats = get_directory_stats(
        current_dir,
        config_data["files"]["max_depth"],
        config_data["files"]["allowed_extensions"],
        config_data["files"]["ignore_patterns"]
    )
    header["stats"] = stats

    # Generate tree
    tree = get_file_tree(current_dir)
    header["tree"] = tree

    # Create final JSON structure
    final_data = {
        "header": header,
        "structure": {}
    }

    # Write to data.json
    try:
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent='\t', ensure_ascii=False)
        print(f"Successfully generated {data_file}")
    except Exception as e:
        print(f"Error writing to data.json: {e}")

if __name__ == "__main__":
    main()

