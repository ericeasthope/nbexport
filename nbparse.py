#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Jupyter notebook parsing and Markdown conversion
Assembled by Eric Easthope

Usage:

```
from nbparse import getNotebooks, nb2md
notebooks = getNotebooks()
for notebook in notebooks.items():
    nb2md(*notebook)
```
'''

import os
import nbformat

from traitlets.config import Config
from nbconvert import MarkdownExporter

MODULE_DIRECTORY =   os.path.dirname(os.path.abspath('__file__'))
NOTEBOOK_DIRECTORY = os.path.join(MODULE_DIRECTORY, '_jupyter')
MARKDOWN_DIRECTORY = os.path.join(MODULE_DIRECTORY, '_posts')
IMAGE_DIRECTORY =    os.path.join(MODULE_DIRECTORY, 'images')

if not os.path.exists(MARKDOWN_DIRECTORY): os.makedirs(MARKDOWN_DIRECTORY)
if not os.path.exists(IMAGE_DIRECTORY):    os.makedirs(IMAGE_DIRECTORY)

def getNotebooks():
    '''
    get notebook paths recursively and overlook temporary files,
    strip path to parent directory and filename extension for each notebook name,
    read in each notebook and create a named dictionary entry with notebook's contents
    '''

    notebooks = {}

    notebook_paths = [os.path.join(directory, file)
        for directory, d, files in os.walk(NOTEBOOK_DIRECTORY)
            for file in files
                if file.endswith('.ipynb')
                and not os.path.splitext(file)[0].endswith('checkpoint')
                ]

    for path in notebook_paths:
        name = path.split('/')[-1].split('.')[0]
        notebook = nbformat.read(path, as_version=nbformat.NO_CONVERT)
        notebooks[name] = notebook

    return notebooks;

def nb2md(name, notebook):
    '''
    get image paths and to each assign a unique key by its respective notebook name,
    write out images to IMAGE_DIRECTORY,
    convert notebook to Markdown and write out Markdown to MARKDOWN_DIRECTORY
    '''

    config = Config()
    config.TemplateExporter.preprocessors = [
        'nbconvert.preprocessors.ExtractOutputPreprocessor'
        ]

    extractOutputConfig = {
        'unique_key': name,
        'output_files_dir': IMAGE_DIRECTORY
        }

    markdown, resources = MarkdownExporter().from_notebook_node(
        notebook,
        resources=extractOutputConfig
        )

    for relative_path, image in resources['outputs'].items():
        image_name = relative_path.split('/')[-1]
        image_path = os.path.join(IMAGE_DIRECTORY, image_name)
        with open(image_path, 'wb') as image_file:
            image_file.write(image)

    markdown_path = os.path.join(MARKDOWN_DIRECTORY, name + '.md')
    with open(markdown_path, 'wb') as markdown_file:
        markdown_file.write(markdown.encode('utf-8'))
