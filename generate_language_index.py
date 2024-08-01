import os
import json
from transformers import pipeline

pipe = pipeline("text-generation", model="microsoft/Phi-3-mini-128k-instruct", trust_remote_code=True, max_length=100)
prompt = "You just tell me the language family of the language I pass to you. Just the name. I don't want any sentences."

path = "docs/eng/"
files = os.listdir(path)
files.sort()
output = {}

for file in files:
    if os.path.isdir(os.path.join(path, file)):            
            continue
    language_name = file.split(".")[0]
    llm_inputs = [
         {
            "role": "system", 
            "content": prompt
          },
         {
              "role": "user", 
              "content": language_name
         },
    ]
    print(pipe(llm_inputs))
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
