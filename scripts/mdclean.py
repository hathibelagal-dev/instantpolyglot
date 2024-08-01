
import os
import re

import fire


here_path = os.path.dirname(os.path.realpath(__file__))
md_path = os.path.join(here_path, '..', 'docs', 'eng')


def nice_quotes(text):
    # "asd" into “asd”
    text = re.sub(r'\"([^\"]*)\"', r'“\1”', text)
    # don't isn't into don’t isn’t etc.
    pairs = [("on't", "on’t"), ("sn't", "sn’t"), ("ren't", "ren’t"), ("an't", "an’t")]  
    for pair in pairs:
        text = text.replace(pair[0], pair[1])
    return text


def clean_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    text = nice_quotes(text)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def clean_all_files():
    print(f'Cleaning all files in {md_path}')
    for root, _, files in os.walk(md_path):
        for file in files:
            if file.endswith('.md'):
                clean_file(os.path.join(root, file))
    print('Done.')


if __name__ == '__main__':
    fire.Fire({
        'nice-quotes': nice_quotes,
        'clean-file': clean_file,
        'clean-all-files': clean_all_files
    })