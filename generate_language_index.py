import os
import json

path = "docs/eng/"
files = os.listdir(path)
files.sort()
output = {}

for file in files:
    language_name = file.split(".")[0]
    output[language_name] = {
        "file_html" : "dist/" + language_name + ".html",
        "file_md" : path + file
    }

with open("language_index.json", "w") as f:
    f.write(json.dumps(output, indent = 4))

list_items = ""

with open("index.html", "w") as f:
    with open("index_template.dat") as template:
        contents = template.read()
        for item in output:
            list_items += f"""
                <li class="list-group-item"><a href="{output[item]["file_html"]}">{item}</a></li>
            """
        contents = contents.replace("#LANGUAGE_INDEX#", list_items)
        contents = contents.replace("#N_LANGUAGES#", str(len(files)))
        f.write(contents)
