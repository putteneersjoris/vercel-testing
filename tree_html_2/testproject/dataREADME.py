#README content using raw string

admin = "Annelotte"
admin_fullname = "Annelotte Lammertse"
user = "student"
domain_name = "https://putteneersjoris.xyz/annelottelammertse"
admin_github_account = "https://github.com/AnnelotteLammertse"
admin_repository_name = "annelottelammertse"

user_github_account = "https://github.com/studentName"
user_repository_name = "annelottelammertse"

# videos and images
# admin
admin_only_once = "./example/admin_only_once.gif"
admin_upload_project = "./example/videos/admin_upload_project.gif"
admin_update_project = "./example/videos/admin_update_project.gif"
admin_remove_project = "./example/videos/admin_remove_project.gif"
admin_approve_project = "./example/videos/admin_approve_project.gif"

admin_confirmation_email = "./example/admin_confirmation_email.jpg"

# user
user_only_once = "./example/user_only_once.gif"
user_fork_repository = "./example/videos/user_fork_repository.gif"
user_update_project = "./example/videos/user_update_project.gif"
user_upload_project = "./example/videos/user_upload_project.gif"
user_remove_project = "./example/videos/user_remove_project.gif"

# naviagtion
navigation = "./example/videos/website_navigation.png"


user_instructions = [
     ["upload", "./example/videos/user_upload_project.gif"],
     ["remove", "./example/videos/user_remove_project.gif"],
     ["update", "./example/videos/user_update_project.gif"]
]

admin_instructions = [
    ["upload", "./example/videos/admin_upload_project.gif"],
    ["remove", "./example/videos/admin_remove_project.gif"],
    ["update", "./example/videos/admin_update_project.gif"],
    ["approve", "./example/videos/admin_approve_project.gif"]
]


#admin_setup
admin_setup = f""" 

# Website: {admin_fullname}

## online@ [{domain_name}]({domain_name})

## instructions: {admin}

"""

#user_setup
user_setup = f""" 

## instructions: {user}

<details>
<summary><u> First setup (only once)</u></summary>
<br>
<ul>   
<li>1. Make sure you have a GitHub account: e.g: <a href="{user_github_account}">{user_github_account}</a></li>
<li>2. Fork the repository located under {admin}'s repository <a href="{admin_github_account}/{admin_repository_name}"> {admin_github_account}/{admin_repository_name}</a>.
<li><img src="./example/videos/user_fork_repository.gif"></li>
</ul>
<br>
</details>

"""

#admin_content
# <a href="{admin_github_account}/{admin_repository_name}/tree/main/src/content"> {admin_github_account}/{admin_repository_name}/tree/main/src/content</a>
admin_content = ""

for i,item in enumerate(admin_instructions):
    admin_content += f"""

<details>
<summary>{i+1}: {item[0]} a project ({admin})</summary>
<br>
<ul>
<li>Please ensure that you are logged in to GitHub.</li>
<li>Go to the content directory: "src/content/".</li>
<li> {item[0]} your project as shown in the following video.<br>
<li><img src="{item[1]}" alt="{item[0]} Project"></li>
<li>You have successfully {item[0]}ed a project. You can preview updates in 'Incognito mode' in your browser. Keep in mind that your browser caches content, so updates may be delayed for some time.</li>
</ul>
<br>
</details>

"""

#user_content

user_content = ""

for i,item in enumerate(user_instructions):
    user_content += f"""

<details>
<summary>{i+1}: {item[0]} a project ({user})</summary>
<br>
<ul>
<li>Please ensure that you are logged in to GitHub.</li>
<li>Go to your instance of {admin}'s website repository contentfolder: "src/content/" </li>
<li>Sync fork (this makes sure you have the latest version so there are no conflicts between other users).</li>
<li>Go to the content folder: ({user_github_account}/{user_repository_name}/tree/main/src/content).</li>
<li> {item[0]} your project as shown in the following video.<br>
<li><img src="{item[1]}" alt="{item[0]} Project"></li>
<li>Contribute by opening up a 'pull request > create pull request'.</li>
<li>Now {admin} will get an email notification, as well as having an open pull request that can be approved or disapproved.</li>
<li>You now have successfully {item[0]}'ed a project. Once {admin} approves of the changes, you can see your project on the official website.</li>
</ul>
<br>
</details>
"""


#demoproject
demoproject_intro = f""" 
## demoproject
In the following section a demoproject is provided.This includes images and a description file. You can the coresponding files <a href="https://github.com/putteneersjoris/annelottelammertse/tree/main/example/demoproject">here</a>

"""
folder_tree = f""" 
```bash
demoproject file tree:

├── project_name
│ ├── 1.jpg
│ ├── 2.jpg
│ ├── 3.jpg
│ ├── 4.jpg
│ ├── 5.jpg
│ └── description.txt

```
"""


#demoproject_images
folder_images = f""" 

### images

- Images can be of `.jpg`, `.png`, `.gif`, `.HEIC` format.
- The max image filezize is 10mb.
- the max resolution is 5000x5000 pixels

<div style="display: flex; flex-wrap: wrap;">
    <img src="./example/demoproject/1.png" width="32%">
    <img src="./example/demoproject/2.png" width="32%">
    <img src="./example/demoproject/3.png" width="32%">
</div>

"""
folder_description = f""" 

### description

- You can only have 1 description. You can upload more but only alphabetically first one will be read.
-  It can have filenames with spaces, and characters.
-  word, or other office documents or any other word processor is not supported. it can only have a .txt file extension. 
-  Every `.txt` file in every project should have 4 tags. `<title></title>`, `<date>,</date>`, `<body></body>`, `<tags></tags>`:

They can be used like this:

```html
<title>Project 1</title> <!-- PROJECTTITLE-->
<date>10/10/2024</date> <!-- PROJECDATE-->
<tags>textile, bioactive, healthcare, wound healing</tags> <!-- TAGS, SEPERATED BY COMMA-->
<body> <!-- MAIN TEXT-->
    <h2>Project Overview</h2> <!-- SUBTITLE-->
    This project focuses on the development of bioactive textiles for applications in wound healing and healthcare. By incorporating bioactive agents into textile fibers, we aim to create functional textiles capable of promoting wound healing, preventing infections, and improving overall healthcare outcomes. The project involves a multidisciplinary approach that combines textile engineering, biomaterials science, and medical research to design innovative solutions for medical textiles.
    The use of bioactive textiles has the potential to revolutionize wound care by providing continuous, localized delivery of therapeutic agents directly to the wound site. This targeted delivery system minimizes systemic side effects and enhances the efficacy of treatment. Additionally, bioactive textiles offer advantages such as improved patient comfort, reduced dressing changes, and simplified wound management procedures.  

    The research objectives of the project include investigating methods for functionalizing textile fibers with bioactive agents, optimizing the release kinetics of therapeutic compounds, and evaluating the biocompatibility and safety of bioactive textiles for clinical use. Advanced fabrication techniques such as electrospinning, coating, and grafting will be employed to incorporate bioactive agents into textile matrices while preserving their structural integrity and mechanical properties.

    <details><summary>Click for more details</summary>This section contains additional details about the project.<!-- EXPANDIBLE SECTION-->
	    <a href="https://www.sciencedirect.com/science/article/pii/S014296121830642X">Read this paper</a> <!-- LINKS-->
	    <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5799424/">Explore this study</a>
	    <a href="https://www.frontiersin.org/articles/10.3389/fbioe.2020.587592/full">Find out more</a> about advanced fabrication techniques for bioactive textiles.</details>
    <details><summary>Click for more details</summary>This section contains additional details about the project.</details>

    <p>The expected outcomes of the project include the development of bioactive textiles with tailored properties for specific medical applications, such as wound dressings, compression garments, and implantable devices. These innovative textiles have the potential to improve patient outcomes, reduce healthcare costs, and advance the field of regenerative medicine.</p><!-- PROJECT PARAGRAPH-->
</body>
```
"""

example_visualized = f""" 
"""


admin_instructions =admin_setup + admin_content
user_instructions =user_setup + user_content
demoproject =demoproject_intro + folder_tree + folder_images + folder_description +  example_visualized

#navigation
navigation_overview = f""" 

## navigation
<img src="./example/videos/website_navigation.gif">
"""

#workflow
workflow = f""" 

## code

Every push request activates a github actions protocal  that:

- installs:
    - imagemagick for image processing
-  generates:
    - the static .html webpages for every project.
    - the data.js file that is needed for script.js
- uploads:
    - script.js
    - index.html

"""


