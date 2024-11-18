import os
import json
import re
import subprocess
import math
from staticHtmlString import html_string

contentFolder = "./content"  # Specify the folder where your content is located
outputFolder = "./"     # Specify the folder where you want to save the HTML files
max_bytes =math.floor( 0.1 * 1048576) # 5mb
processed_addition = "__processed"
approved_extensions = ("jpg", "png", "jpeg", "txt", "gif", "heic")

# Functions

def decompose_file(file_path):
	parts = file_path.rsplit("/", 1)
	directory = parts[0]
	filename_with_extension = parts[1]
	filename_without_extension, extension = filename_with_extension.split(".", 1)
	
	return directory, filename_with_extension, filename_without_extension, extension



def rename_file(file_path):
	#replace spaces in file with _
	directory, filename_with_extension=  decompose_file(file_path)[:2]
	file_no_spaces = os.path.join( directory, filename_with_extension.replace(" ", "_").replace("(","_").replace(")","_").replace("{","_").replace("}","_") )
	os.rename( file_path , file_no_spaces )

	return file_no_spaces



def rename_file_processed(file_path):
	#if file has good res and size, we can rename it to __processed
	directory, filename_with_extension, filename_without_extension, extension=  decompose_file(file_path)
	file_processed = os.path.join( directory, filename_without_extension + processed_addition  + "." + extension  )
	os.rename( file_path , file_processed)

def remove_unsupported_file(file_path):
	extension=  decompose_file(file_path)[-1]
	if extension.lower() not in approved_extensions:
		os.remove(file_path)
		print(f'{file_path} is not supported and has been removed.')
		return True
	else:
		return False


def process_images(file_path):
	optional_args = ""
	processed_extension = ""
	
	extension = decompose_file(file_path)[-1]

	if extension.lower() == "heic":
		processed_extension = "png"
		optional_args = "-resize '1024x>' -quality 80"

	if extension.lower() == "gif":
		processed_extension = "gif"
		optional_args = "-resize '512x>' -quality 80"

	if extension.lower() in ("png", "jpg", "jpeg", "jpeg"):
		processed_extension = "png"
		optional_args = "-resize '1024x>' -quality 80"
	
	return optional_args, processed_extension


def process_files(file_path, max_bytes):
		
	if remove_unsupported_file(file_path):
		return

	directory, filename_with_extension, filename_without_extension, extension = decompose_file(file_path)

	if extension != "txt":
		if processed_addition  in filename_without_extension:
			return
		
		file_size = os.path.getsize(file_path)
		
		if file_size >= max_bytes:

			optional_args,processed_extension = process_images(file_path) 
			
			file_path_reconstructed = f"{directory}/{filename_without_extension}.{extension}"
			file_dir_reconstructed = f"{directory}/"
			
			command  = f"convert \"{file_path_reconstructed}\" {optional_args} -set filename:base '%[basename]' \"{file_dir_reconstructed}%[filename:base]_{processed_addition}.{processed_extension}\""
			
			subprocess.run(command, shell=True)
			
			os.remove(file_path) #remove original file afterwards
			
		else:
			rename_file_processed(file_path)


##process images
for folder in os.listdir(contentFolder):
	folder_path = os.path.join(contentFolder, folder)
	if os.path.isdir(folder_path):
		for file in os.listdir(folder_path):
			file_path = os.path.join(folder_path, file)
			process_files(rename_file(file_path), max_bytes)




#process .txt file to html

#cleanup first
# Delete all .html files (excluding index.html) in the output folder
for filename in os.listdir(outputFolder):
	filepath = os.path.join(outputFolder, filename)
	if filename.endswith(".html") and filename != "index.html":
		os.remove(filepath)
  

# Initialize arrays for images, tags, date, projects, allTags, and barContent
images = []
tags = []
date = []
projects = {}
allTags = []
barContent = []
htmlFiles = []

# make array with all projectnames
for folderName in os.listdir(contentFolder):
	folderPath = os.path.join(contentFolder, folderName)
	htmlFiles.append(folderName)

sorted_htmlFiles = sorted(htmlFiles)

# Iterate through the content folder
for i,folderName in enumerate(sorted(os.listdir(contentFolder))):
	# loop through sorted html_files so we can pick i+1 and i-1 fo to back and fort
	next_index = (i + 1) % len(sorted_htmlFiles)
	next_htmlFile = "./" + sorted_htmlFiles[next_index] + ".html"
	previous_index = (i - 1) % len(sorted_htmlFiles)
	previous_htmlFile = "./" + sorted_htmlFiles[previous_index] + ".html"

	folderPath = os.path.join(contentFolder, folderName)
	if os.path.isdir(folderPath):
		project_images = []
		project_tags = []
		project_date = []
		project_html = ""


		for item in os.listdir(folderPath):
			itemPath = os.path.join(folderPath, item)

			if os.path.isfile(itemPath):
				#if item.endswith(".gif"):
					#images.append(itemPath)
					#project_images.append(itemPath)

				if item.endswith((".jpg", ".png", ".heic", ".gif")):
					#itemPath_base = os.path.splitext(os.path.basename(itemPath))[0]
					#itemPath_ext = os.path.splitext(os.path.basename(itemPath))[1]
					#itemPath_resized = os.path.join(folderPath,itemPath_base + "_resized" + itemPath_ext)
					#os.system(f'convert "{itemPath}"  -sharpen 0x.2 -resize x350 "{itemPath}"')
					images.append(itemPath)
					project_images.append(itemPath)

				elif item.endswith(".txt"):
					with open(itemPath, 'r') as txt_file:
						content = txt_file.read()
						date_match = re.search(r'<date>(.*?)<\/date>', content, re.DOTALL)
						if date_match:
							project_date.append(date_match.group(1).strip())
							project_date = date_match.group(1).strip()
						body_match = re.search(r'<body>(.*?)<\/body>', content, re.DOTALL)
						if body_match:
							project_html = body_match.group(1).strip()
							project_html = project_html.replace('\n', '<br>')
                        
						tags_match = re.search(r'<tags>(.*?)<\/tags>', content, re.DOTALL)
						if tags_match:
							tags_content = tags_match.group(1).strip()
							tags_formatted = ["#" + tag.strip() + "<br>" for tag in tags_content.split(',')]
							allTags.extend([
								"<span class='filter' data-filter='" + tag.strip() + "'>#" + tag.strip() + "</span>"
								for tag in tags_content.split(',')
							])
							# print(allTags)
					#break out of the loop after procvessing the first file
					break

		tag_list = [f"<span>#{tag.strip()}</span><br>" for tag in tags_content.split(",")]
		tag_string = "".join(tag_list)
		project_tags.append(tag_string)
		# print(project_tags)           
                
		project_images.sort()  # Sort the image paths for the current project
        
		projects[folderName] = {
			"images": project_images,
			"html": project_html,
			"tags": project_tags,
			"date": project_date
		}
        
		#print(tags_content)

		# Create a project HTML file with images and barContent links
		images_html = "\n".join([f"<img class='imagesPage'  src='{image_path}' >" for image_path in project_images])
		num_images =3	
		
		#html string comes from staticHtmlString
		project_html_content = html_string(folderName, project_date, previous_htmlFile, next_htmlFile, tag_string, project_html, images_html, num_images)


		project_html_path = os.path.join(outputFolder, f"{folderName}.html")
		with open(project_html_path, 'w') as project_html_file:
			project_html_file.write(project_html_content)

allTags = list(set(allTags))
allTags.sort()

# Sort the project names
sorted_project_names = sorted(projects.keys())

# Create the barContent array with formatted project names
formatted_barContent = [
	"<a href='./" + project_name + ".html'>" + project_name + "</a>&ensp;&ensp;"
	for project_name in sorted_project_names
]

# Duplicate the formatted_barContent array 10 times
duplicated_barContent = formatted_barContent * 10

# Create the content dictionary with sorted projects
sorted_projects = {project_name: projects[project_name] for project_name in sorted_project_names}

# Create the content dictionary
content = {
	"projects": sorted_projects,
	"allTags": allTags,
	"barContent": duplicated_barContent
}

# Convert the content dictionary to JSON format
content_json = json.dumps(content, indent=4)

# Write the JSON content to a file named "dataB.js"
with open("data.js", "w") as file:
	file.write("var content = ")
	file.write(content_json)

print("File 'data.js' saved successfully.")

