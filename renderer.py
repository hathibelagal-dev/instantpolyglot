import os
import mistune
from mistune.plugins.table import table

path = "docs/eng/"
files = os.listdir(path)
to_replace = "#MARKDOWN#"
output_path1 = "dist/"
output_path2 = "articles/"
markdown = mistune.create_markdown(plugins=[table, 'footnotes', 'strikethrough'])
with open("render_template.dat") as template:
    template_contents = template.read()
    for file in files:
        output_file_path1 = output_path1 + file.split(".")[0] + ".html"
        output_file_path2 = output_path2 + file.split(".")[0] + ".html"
        with open(path + file) as f:
            md = f.read()
            rendered = markdown(md)
            generated_html = template_contents.replace(to_replace, rendered).replace("#LANGUAGE_NAME#", file.split(".")[0])
            with open(output_file_path1, "w") as output_file:
                output_file.write(generated_html)
            with open(output_file_path2, "w") as output_file:
                output_file.write(generated_html)
