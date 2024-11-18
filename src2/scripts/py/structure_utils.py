import os
from pathlib import Path
import datetime
from config_utils import get_config_value
from logger import log_message

def get_timestamps(path):
    """Get creation and modification timestamps for a path."""
    try:
        stats = os.stat(path)
        # Convert timestamps to ISO format
        created = datetime.datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%dT%H:%M:%SZ')
        modified = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%dT%H:%M:%SZ')
        return created, modified
    except Exception as e:
        return "1970-01-01T00:00:00Z", "1970-01-01T00:00:00Z"

def get_image_paths(root_path, current_path):
    """Get all image paths under the current path."""
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif'}
    images = []
    
    try:
        for root, _, files in os.walk(current_path):
            for file in files:
                if os.path.splitext(file)[1].lower() in image_extensions:
                    # Create path relative to root
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, root_path)
                    images.append('/' + rel_path.replace('\\', '/'))
    except Exception as e:
        log_message(None, f"Error getting image paths: {e}")
    
    return images

def create_content_section(path, root_path, is_directory=True):
    """Create the content section for a file or directory."""
    html_path = '/' + os.path.relpath(path, root_path).replace('\\', '/')
    if is_directory:
        html_path = os.path.join(html_path, 'index.html').replace('\\', '/')
    
    return {
        "dir_tree": {},
        "html_content": {
            "custom_html_present": True,  # TODO: Check for actual .html files
            "htmlPath": html_path
        },
        "threejs_scene": {
            "images": get_image_paths(root_path, path),
            "tags": {
                "stack_tag": [],
                "comment_tag": []
            }
        }
    }

def should_ignore(name, ignore_patterns):
    for pattern in ignore_patterns:
        if pattern.endswith('*'):
            if name.startswith(pattern[:-1]):
                return True
        elif pattern.startswith('*'):
            if name.endswith(pattern[1:]):
                return True
    return False

def get_file_type(filename):
    ext = os.path.splitext(filename)[1].lower().lstrip('.')
    file_type_mapping = {
        'md': 'markdown',
        'js': 'javascript',
        'py': 'python',
        'html': 'html',
        'css': 'css',
        'json': 'json',
        'yml': 'yaml',
        'txt': 'text',
        'png': 'image',
        'jpg': 'image',
        'gif': 'image',
        'mp4': 'video',
    }
    return file_type_mapping.get(ext, 'unknown')

def calculate_directory_size(structure):
    total_size = 0
    if not structure or 'children' not in structure:
        return 0
    for child in structure['children'].values():
        if child['type'] == 'file':
            total_size += child['file_metadata']['size']
        elif child['type'] == 'directory':
            total_size += calculate_directory_size(child)
    return total_size

def process_directory(path, config, current_depth=0, parent_id=0, log_file=None):
    if current_depth > get_config_value(config, 'files', 'max_depth', default=5):
        return None

    root_path = get_config_value(config, 'paths', 'root', default='./')
    allowed_extensions = get_config_value(config, 'files', 'allowed_extensions', default=[])
    ignore_patterns = get_config_value(config, 'files', 'ignore_patterns', default=[])
    
    log_message(log_file, f"\nProcessing directory: {path}")
    
    dir_name = os.path.basename(path) or "root"
    created, modified = get_timestamps(path)
    
    structure = {
        "name": dir_name,
        "type": "directory",
        "htmlPath": '/' + os.path.relpath(path, root_path).replace('\\', '/') + '/index.html',
        "folder_metadata": {
            "childCount": 0,
            "size": 0,
            "created": created,
            "lastModified": modified
        },
        "content": create_content_section(path, root_path),
        "children": {}
    }

    try:
        items = os.listdir(path)
        child_id = 0
        
        # Process directories first
        for item in sorted(items):
            item_path = os.path.join(path, item)
            
            if should_ignore(item, ignore_patterns):
                log_message(log_file, f"Ignoring item: {item}")
                continue

            if os.path.isdir(item_path):
                child_result = process_directory(
                    item_path, 
                    config, 
                    current_depth + 1,
                    child_id,
                    log_file
                )
                if child_result:
                    structure["children"][item] = child_result
                    child_id += 1
                    structure["folder_metadata"]["childCount"] += 1

        # Then process files
        for item in sorted(items):
            item_path = os.path.join(path, item)
            
            if should_ignore(item, ignore_patterns):
                continue

            if os.path.isfile(item_path):
                ext = os.path.splitext(item)[1].lower().lstrip('.')
                if ext in allowed_extensions:
                    try:
                        file_size = os.path.getsize(item_path)
                    except OSError:
                        file_size = 0
                        
                    created, modified = get_timestamps(item_path)
                    
                    structure["children"][item] = {
                        "name": item,
                        "type": "file",
                        "fileType": get_file_type(item),
                        "htmlPath": '/' + os.path.relpath(item_path, root_path).replace('\\', '/'),
                        "file_metadata": {
                            "childId": child_id,
                            "size": file_size,
                            "created": created,
                            "lastModified": modified
                        },
                        "content": create_content_section(item_path, root_path, is_directory=False)
                    }
                    child_id += 1
                    structure["folder_metadata"]["childCount"] += 1

        # Calculate total directory size after processing all children
        structure["folder_metadata"]["size"] = calculate_directory_size(structure)
        
        log_message(log_file, f"Processed {structure['folder_metadata']['childCount']} items in {path}")
        log_message(log_file, f"Total directory size: {structure['folder_metadata']['size']} bytes")
        
        return structure

    except Exception as e:
        log_message(log_file, f"Error processing directory {path}: {e}")
        return None

def create_structure(config, log_file):
    root_path = get_config_value(config, 'paths', 'root', default='./')
    log_message(log_file, f"\n=== Creating File Structure ===")
    log_message(log_file, f"Starting from root: {root_path}")
    
    structure = {
        "root": process_directory(root_path, config, log_file=log_file)
    }
    
    return structure
