import re
import os
from datetime import datetime

def get_file_type_color(filename):
    """Return color based on file type using RGB colors"""
    # Images
    if re.search(r'\.(jpg|jpeg|png|gif|bmp|svg|webp|mp4|mp3)$', filename.lower()):
        return 'rgb(255,100,255)'
    
    # Archives/Important
    elif re.search(r'\.(zip|tar|gz|rar|7z)$', filename.lower()):
        return 'rgb(255, 0, 0)'
    
    # Executables
    elif re.search(r'\.(exe|sh|bat)$', filename.lower()):
        return 'rgb(0, 255, 0)'
    
    # Code files
    elif re.search(r'\.(py|js|html|css|cpp|java|php|pyc|hiplc)$', filename.lower()):
        return 'rgb(255,255, 255)'
    
    # Documents
    elif re.search(r'\.(pdf|doc|docx|txt|md|csv|json|ttf)$', filename.lower()):
        return 'rgb(255, 255, 255)'
    
    return 'rgb(100,100, 255)'  # Default white

def parse_tree_output(input_file):
    """Parse the tree command output and convert to HTML with colors"""
    with open(input_file, 'r') as f:
        lines = f.readlines()

    html_content = []
    html_content.append("""
<!DOCTYPE html>
<html>
<head>
    <title>Directory Tree</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Ubuntu+Mono:wght@400;700&display=swap');
        
        body {
            background-color: rgb(0, 0, 0);
            color: rgb(255, 255, 255);
            font-family: 'Ubuntu Mono', monospace;
            padding: 20px;
            font-size: 14px;
        }
        .tree-line {
            white-space: pre;
            margin: 0;
            line-height: 1.2;
            height: 1.2em;
            display: flex;
            align-items: center;
        }
        .tree-structure {
            color: rgb(255, 255, 255);
        }
        .tree-name {
            margin-left: -1px;
        }
        details {
            margin-left: 0;
        }
        summary {
            display: flex;
            align-items: center;
            cursor: pointer;
            list-style: none;
        }
        summary::-webkit-details-marker {
            display: none;
        }
        summary::before {
            font-family: 'Font Awesome 6 Free';
            content: '\\f105';
            color: rgb(255, 255, 255);
            margin-right: 4px;
            font-size: 12px;
            transition: transform 0.2s;
            width: 12px;
            font-weight: 900;
        }
        details[open] > summary::before {
            content: '\\f107';
        }
        summary:hover::before {
            color: rgb(255, 255, 255);
        }
        .folder-content {
            margin-left: 0;
        }
        h2 {
            color: rgb(255, 255, 255);
            font-size: 16px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h2>Directory Tree Generated on """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</h2>
    <div class="tree-content">
    """)

    # Process lines and track indentation
    current_indent = 0
    indent_stack = []
    
    for line in lines:
        line = line.rstrip()
        if not line:
            continue

        # Get the indentation level
        indent = len(line) - len(line.lstrip())
        indent_level = indent // 4

        # Close previous details tags if we're moving back up the tree
        while indent_stack and indent_stack[-1] >= indent_level:
            html_content.append('</details>')
            indent_stack.pop()

        # Split the line into structure and name parts
        match = re.match(r'^(.*?[└├]──\s*)(.*?)$', line)
        if match:
            structure, name = match.groups()
        else:
            structure, name = '', line

        # Format the structure part
        structure = structure.replace('\\', '│').replace('└──', '└──').replace('├──', '├──')

        # Check if it's a directory (excluding the "X directories, Y files" line)
        is_directory = (name.endswith('/') or '[' in name) and not 'directories' in line

        if is_directory:
            # Handle directory lines
            html_content.append(
                f'<details open>'
                f'<summary class="tree-line">'
                f'<span class="tree-structure">{structure}</span>'
                f'<span class="tree-name" style="color: rgb(0, 0, 255)">{name}</span>'  # Blue
                f'</summary>'
                f'<div class="folder-content">'
            )
            indent_stack.append(indent_level)
        else:
            # Handle file lines
            color = get_file_type_color(name)
            html_content.append(
                f'<div class="tree-line">'
                f'<span class="tree-structure">{structure}</span>'
                f'<span class="tree-name" style="color: {color}">{name}</span>'
                f'</div>'
            )

    # Close any remaining open details tags
    for _ in indent_stack:
        html_content.append('</details>')

    html_content.append("""
    </div>
</body>
</html>
    """)

    return '\n'.join(html_content)

def create_html_tree(input_file='output.txt', output_file='index.html'):
    """Main function to create HTML file from tree output"""
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return
    
    html_content = parse_tree_output(input_file)
    
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"Successfully created {output_file}")

if __name__ == "__main__":
    create_html_tree()
