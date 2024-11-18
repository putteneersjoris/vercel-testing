import os
from PIL import Image
from config_utils import get_config_value
from logger import log_message

def get_image_dimensions(config):
    """Get image dimensions from config for different contexts."""
    return {
        'html_desktop': get_config_value(config, 'media', 'html_content', 'dimensions', 'desktop', default=[800, 600]),
        'html_mobile': get_config_value(config, 'media', 'html_content', 'dimensions', 'mobile', default=[800, 600]),
        'threejs_desktop': get_config_value(config, 'media', 'threejs_scene', 'dimensions', 'desktop', default=[800, 600]),
        'threejs_mobile': get_config_value(config, 'media', 'threejs_scene', 'dimensions', 'mobile', default=[800, 600])
    }

def get_processed_paths(config, root_path):
    """Get paths for processed images."""
    return {
        'html_desktop': os.path.join(root_path, '.html_desktop_processed'),
        'html_mobile': os.path.join(root_path, '.html_mobile_processed'),
        'threejs_desktop': os.path.join(root_path, '.threejs_desktop_processed'),
        'threejs_mobile': os.path.join(root_path, '.threejs_mobile_processed')
    }

def create_processed_directories(paths):
    """Create directories for processed images."""
    for path in paths.values():
        os.makedirs(path, exist_ok=True)
        # Create parent directories too
        parent_dir = os.path.dirname(path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

def resize_image(image_path, output_path, dimensions, log_file):
    """Resize image maintaining aspect ratio."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with Image.open(image_path) as img:
            # Use ANTIALIAS for older PIL versions, LANCZOS for newer
            try:
                resampling = Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS
            except AttributeError:
                resampling = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.ANTIALIAS
            
            img.thumbnail(dimensions, resampling)
            img.save(output_path, quality=95, optimize=True)
            log_message(log_file, f"Resized {image_path} to {dimensions}")
    except Exception as e:
        log_message(log_file, f"Error processing {image_path}: {e}")

def process_images(config, log_file):
    """Process all images in directory structure."""
    root_path = get_config_value(config, 'paths', 'root', default='./')
    dimensions = get_image_dimensions(config)
    processed_paths = get_processed_paths(config, root_path)
    create_processed_directories(processed_paths)
    
    log_message(log_file, "\n=== Processing Images ===")
    log_message(log_file, f"Root path: {root_path}")
    log_message(log_file, f"Processing paths: {processed_paths}")
    
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif'}
    processed_image_paths = []
    
    for root, _, files in os.walk(root_path):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, root_path)
                log_message(log_file, f"\nProcessing image: {rel_path}")
                
                # Preserve directory structure in processed folders
                for context, proc_path in processed_paths.items():
                    output_path = os.path.join(proc_path, rel_path)
                    dimensions_key = context.replace('_processed', '')
                    resize_image(src_path, output_path, dimensions[dimensions_key], log_file)
                    processed_image_paths.append(output_path)
    
    log_message(log_file, f"\nProcessed {len(processed_image_paths)} images")
    return processed_paths
