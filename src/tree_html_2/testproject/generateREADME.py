#this script generates the README file for annelotte's website.
# you run this script by `python generateREADME.py`. this will write a custom readme file
# tho change the content of the file, this can be found in dataREADME.py under the many variables


import os
from dataREADME import ( admin_instructions, user_instructions, demoproject, navigation_overview, workflow )


# Define paths to files and directories
basedir = os.getcwd()
src_folder = os.path.join(basedir, "src")
actions_folder = os.path.join(basedir, ".github/workflows/")


file_paths = [
    os.path.join(actions_folder, "default.yaml"),
    os.path.join(src_folder, "index.html"),
    os.path.join(src_folder, "staticHtmlString.py"),
    os.path.join(src_folder, "generateData.py"),
    os.path.join(src_folder, "data.js"),
    os.path.join(src_folder, "script.js"),
    os.path.join(src_folder, "style.css")
]


readme_content = admin_instructions + user_instructions + demoproject + navigation_overview


# Function to read file content
def read_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()


for i,file_path in enumerate(file_paths):
    if os.path.exists(file_path):
        file_name = os.path.basename(file_path)
        file_content = read_file_content(file_path)
        is_default = os.path.basename(file_path) == "default.yaml"
        open_attribute = " open " if is_default else ""
        workflow += f'\n\n<details {open_attribute}><summary>{i}: {file_name}</summary>\n\n```\n{file_content}\n```\n</details>\n\n'

readme_content +=workflow

# Write README file
with open('README.md', 'w') as readme_file:
    readme_file.write(readme_content)

print("Readme generated successfully: README.md")







