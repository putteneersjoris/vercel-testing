def html_string(folderName, project_date, previous_htmlFile, next_htmlFile, tag_string, project_html, images_html, num_images):
    project_html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Annelotte Lammertse</title>
    <link rel="stylesheet" href="./style.css">
</head>
<body>
    <span id="tags-wrapper"></span> <!-- set tags here > -->
    <div id="header">
        <div id="title">
            <h1>
                <a href="./index.html" style="color: black; text-decoration: none;">Annelotte Lammertse</a>
            </h1>
        </div>
        <div id="bar">
            <div id="barContent"></div> <!-- set bar content projects here > -->
        </div>
        <div id="contentPage">
            <div id="textPage">
                <h1>{folderName} <br><span style="font-size:14px">{project_date}</span></h1>  <!-- add back, next, and menu buttons here -->
                <div class="containerStatic">
                    <div class="menuprevnext">
                        <span>
                            <a href='./index.html' class='backButtonPage'> menu</a>
                        </span>
                        <br>
                        <span>
                            <a href='{previous_htmlFile}' class='backButtonPage'>previous</a>
                        </span>
                        <br>
                        <span>
                            <a href= '{next_htmlFile}' class='backButtonPage'>next</a>
                        </span>
                    </div>
                    <span id="tagStatic" style="color:rgb(0,0,0);">
                        {tag_string}
                    </span>
                </div>
                <body>
                    <p>{project_html}</p>  <!-- body text here -->
                </body>
            </div>
            <div id="imagePage"> <!-- add all images here -->
                {images_html}
            </div>
        </div>
        <div id="footer">
            <span> Annelotte Lammertse </span>
            <span id="footerTextRight"></span>
        </div>
    </div>
</body>

<script src="data.js"></script> 
<script src="script.js"></script> 

<script>
    document.addEventListener('DOMContentLoaded', function () {{
        // Apply fullscreen styles to images if less than 4 on startup; toggle on click otherwise
        const images = document.querySelectorAll('.imagesPage');
        images.forEach((img, index) => {{
            img.addEventListener('click', () => {{
                img.classList.toggle('imagePageFull');
                img.style.width = img.classList.contains('imagePageFull') ? "100%" : "32.8%";
            }});

            if (images.length < {num_images}) {{
                img.classList.add('imagePageFull');
                img.style.width = "100%";
            }} else if (images.length > {num_images} && index == 0) {{
                img.classList.add('imagePageFull');
                img.style.width = "100%";
            }}
        }});

        // Make the tags that are present red
        var tagsWrapper = document.getElementById('tags-wrapper');
        var tagStaticElements = document.getElementById('tagStatic').getElementsByTagName('span');
        var innerTagArray = [];
        for (var i = 0; i < tagStaticElements.length; i++) {{
            innerTagArray.push(tagStaticElements[i].innerHTML.replace('#', ''));
        }}

        var tags = tagsWrapper.getElementsByTagName('span');
        for (var i = 0; i < tags.length; i++) {{
            var dataFilter = tags[i].getAttribute('data-filter');
            if (innerTagArray.includes(dataFilter)) {{
                tags[i].style.pointerEvents = 'none';
                //tags[i].style.textDecoration = 'underline';
            }} else {{
                tags[i].style.color = 'rgba(0,0,0,0.1)'
                tags[i].style.textDecoration = 'line-through';
            }}
        }}
    }});
</script>
</html>
"""

    return project_html_content
