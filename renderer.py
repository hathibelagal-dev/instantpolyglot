import os
import markdown

path = "docs/eng/"
files = os.listdir(path)
to_replace = "#MARKDOWN#"
output_path = "dist/"
with open("render_template.dat") as template:
    template_contents = template.read()
    for file in files:
        output_file_path = output_path + file.split(".")[0] + ".html"
        with open(path + file) as f:
            md = f.read()
            rendered = markdown.markdown(md)
            generated_html = template_contents.replace(to_replace, rendered)
            with open(output_file_path, "w") as output_file:
                output_file.write(generated_html)
