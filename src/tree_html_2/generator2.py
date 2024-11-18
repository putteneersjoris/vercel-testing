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

def get_directory_stats(start_path, max_depth, allowed_extensions, ignore_patterns):
    """Calculate directory statistics."""
    total_files = 0
    total_folders = 0
    total_size = 0
    last_modified = None
    
    print(f"\nStarting directory scan at: {start_path}")
    print(f"Max depth: {max_depth}")
    print(f"Allowed extensions: {allowed_extensions}")
    print(f"Ignore patterns: {ignore_patterns}")

    # Convert allowed_extensions to lowercase for case-insensitive comparison
    allowed_extensions = [ext.lower() for ext in allowed_extensions]
    
    for root, dirs, files in os.walk(start_path):
        # Calculate current depth
        rel_path = os.path.relpath(root, start_path)
        current_depth = len(rel_path.split(os.sep)) if rel_path != '.' else 0
        
        print(f"\nProcessing directory: {root}")
        print(f"Current depth: {current_depth}")

        # Skip if we're too deep
        if current_depth > max_depth:
            print(f"Skipping - exceeded max depth {max_depth}")
            dirs.clear()  # Don't traverse deeper
            continue

        # Filter out ignored directories before counting
        dirs[:] = [d for d in dirs if not any(
            ignore_pat.replace('*', '') in d
            for ignore_pat in ignore_patterns
        )]
        
        # Count folders after filtering
        total_folders += len(dirs)
        print(f"Added {len(dirs)} folders to count")
        print(f"Current folders: {dirs}")

        # Process files
        for file in files:
            # Get the lowercase extension (including the dot)
            file_ext = os.path.splitext(file)[1].lower()
            
            # Skip files that match ignore patterns
            if any(ignore_pat.replace('*', '') in file for ignore_pat in ignore_patterns):
                print(f"Skipping ignored file: {file}")
                continue

            # Check if file extension is allowed (with and without dot)
            if not (file_ext in allowed_extensions or file_ext[1:] in allowed_extensions):
                print(f"Skipping file with unallowed extension: {file} (ext: {file_ext})")
                continue

            file_path = os.path.join(root, file)
            try:
                # Get file stats
                file_stat = os.stat(file_path)
                total_files += 1
                total_size += file_stat.st_size
                
                # Update last modified time if newer
                if last_modified is None or file_stat.st_mtime > last_modified:
                    last_modified = file_stat.st_mtime
                
                print(f"Processed file: {file} (size: {file_stat.st_size})")
            except OSError as e:
                print(f"Error processing file {file}: {e}")
                continue

    print("\nFinal Statistics:")
    print(f"Total files: {total_files}")
    print(f"Total folders: {total_folders}")
    print(f"Total size: {total_size}")
    print(f"Last modified: {time.strftime('%H_%M_%S', time.localtime(last_modified)) if last_modified else '00_00_00'}")

    return {
        "total_files": total_files,
        "total_folders": total_folders,
        "total_size": total_size,
        "last_modified": time.strftime("%H_%M_%S", time.localtime(last_modified)) if last_modified else "00_00_00"
    }

def get_formatted_datetime():
    """Get current date and time in separate formats."""
    now = datetime.datetime.now()
    return {
        "date": now.strftime("%Y_%m_%d"),
        "timestamp": now.strftime("%H_%M_%S")
    }

def main():
    current_dir = os.getcwd()
    data_file = Path("data.json")
    
    # Get new build ID
    build_id = increment_build_id()
    print(f"Incrementing build ID to: {build_id}")
    
    # Read config.yml
    try:
        with open("config.yml", 'r') as file:
            config_data = yaml.safe_load(file)
    except Exception as e:
        print(f"Error reading config.yml: {e}")
        return

    # Get version from config file or use default
    version = config_data.get("info", {}).get("version", "0.0.1")
    print(f"Using version: {version} from config file")

    # Get current date and time
    datetime_info = get_formatted_datetime()
    print(f"Current date: {datetime_info['date']}")
    print(f"Current timestamp: {datetime_info['timestamp']}")

    # Initialize header structure with all sections
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
            current_dir,
            config_data["files"]["max_depth"],
            config_data["files"]["allowed_extensions"],
            config_data["files"]["ignore_patterns"]
        ),
        "tree": get_file_tree(current_dir),
        "config": {
            "files": config_data["files"],
            "display": config_data["display"],
            "paths": config_data["paths"]
        },
        "media": config_data["media"],
        "dir_tree": config_data["dir_tree"],
        "html_content": config_data["html_content"],
        "threejs_scene": config_data["threejs_scene"]
    }

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

