#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Jupyter notebook parsing and Markdown conversion
Assembled by Eric Easthope
'''

import os
import nbformat
import datetime
import types

from nbconvert import MarkdownExporter
from ruamel.yaml import YAML
from shutil import copy2

MODULE_DIRECTORY =   os.path.dirname(os.path.abspath('__file__'))
NOTEBOOK_DIRECTORY = os.path.join(MODULE_DIRECTORY, '_jupyter')
MARKDOWN_DIRECTORY = os.path.join(MODULE_DIRECTORY, '_posts')
IMAGE_DIRECTORY =    os.path.join(MODULE_DIRECTORY, 'images')

class Parser(object):
    def __init__(self):
        self.names = []
        self.notebooks = []

    def get_notebooks(self):
        '''
        get notebook paths recursively and overlook temporary files,
        strip path to parent directory and filename extension for each notebook name,
        read in each notebook and create a named dictionary entry with notebook's contents
        '''

        if not os.path.isdir(NOTEBOOK_DIRECTORY):
            print('Warning: _jupyter directory not found ...')
            print('No notebooks were converted.')

        notebook_paths = [os.path.join(directory, file)
            for directory, d, files in os.walk(NOTEBOOK_DIRECTORY)
                for file in files
                    if file.endswith('.ipynb')
                    and not os.path.splitext(file)[0].endswith('checkpoint')
                    ]

        for path in notebook_paths:
            name = path.split('/')[-1].split('.')[0]
            notebook = nbformat.read(path, as_version=nbformat.NO_CONVERT)
            date_modified = datetime.datetime.fromtimestamp(os.path.getmtime(path))
            try:
                date_created = datetime.datetime.fromtimestamp(os.stat(path).st_birthtime)
            except:
                print('No creation date for', name + '.md', 'skipping ...')
                date_created = None

            self.names += [name]
            self.notebooks += [{
                'notebook': notebook,
                'path': path,
                'date_created': '{}-{}-{}'.format(
                    date_created.year,
                    date_created.month,
                    date_created.day
                    ) if date_created is not None else None,
                'date_modified': '{}-{}-{}'.format(
                    date_modified.year,
                    date_modified.month,
                    date_modified.day
                    )
                }]

    def nb2md(self, include_front_matter=True):
        for name, notebook in zip(self.names, self.notebooks):
            '''convert notebook to Markdown and write out Markdown to MARKDOWN_DIRECTORY'''
            markdown, resources = MarkdownExporter().from_notebook_node(notebook['notebook'])

            post_paths = os.listdir(MARKDOWN_DIRECTORY)
            for path in post_paths:
                if path.split('-')[-1].split('.')[0] == name:
                    markdown_path = os.path.join(MARKDOWN_DIRECTORY, path)
                    print('Updating', path.split('-')[-1], '...')
                    break
                else:
                    markdown_path = os.path.join(MARKDOWN_DIRECTORY, notebook['date_modified'] + '-' + name + '.md')

            if len(post_paths) == 0:
                markdown_path = os.path.join(MARKDOWN_DIRECTORY, notebook['date_created'] + '-' + name + '.md')

            if not os.path.exists(MARKDOWN_DIRECTORY):
                os.makedirs(MARKDOWN_DIRECTORY)

            with open(markdown_path, 'wb') as markdown_file:
                if include_front_matter:
                    self._add_front_matter(name, notebook, markdown_file)
                markdown_file.write(markdown.encode('utf-8'))

    def _add_front_matter(self, name, notebook, markdown_file):
        header = notebook['notebook']['cells'][0]['source'].split('\n')
        data = '''\
            layout: post
            title:
            tags:
            '''

        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent(sequence=4, offset=2)
        front_matter = yaml.load(data)

        for h in header:
            if h.startswith('[//]'):
                hash_tags = h[h.find('(')+1:h.find(')')]
                front_matter['tags'] = (hash_tags.replace('#', '')
                                                 .split())
            elif h.startswith('# '):
                front_matter['title'] = h.replace('# ', '').strip()

        front_matter['date'] = notebook['date_modified']

        yaml.dump(front_matter, markdown_file)
        markdown_file.write('---\n'.encode('utf-8'))

    def format_math(self):
        for name, notebook in zip(self.names, self.notebooks):
            for cell in notebook['notebook']['cells']:
                source = cell['source']
                if '$' in source:
                    source_out = source.replace('$$', '\n$$\n')
                    source_out = source_out.replace('$', '$$')
                    source_out = source_out.replace('$$$$', '$$')
                    cell['source'] = source_out

    def format_javascript(self):
        for name, notebook in zip(self.names, self.notebooks):
            for cell in notebook['notebook']['cells']:
                try:
                    if cell['outputs'] != []:
                        js = cell['outputs'][0]['data']['application/javascript']
                        cell['outputs'][0]['data']['text/plain'] = (
                            '<script>'  + '\n' +
                            js          + '\n' +
                            '</script>'
                            )
                except KeyError:
                    pass

    def _copy_image(self, image_name):
        for directory, d, files in os.walk(NOTEBOOK_DIRECTORY):
            for f in files:
                if f.endswith(image_name):
                    image_path = os.path.join(directory, f)
                    break

        if not os.path.exists(IMAGE_DIRECTORY):
            os.makedirs(IMAGE_DIRECTORY)
        copy2(image_path, IMAGE_DIRECTORY)

    def format_image_links(self):
        for name, notebook in zip(self.names, self.notebooks):
            for cell in notebook['notebook']['cells']:
                source = cell['source']
                if source.startswith('![](') and source.endswith(')'):
                    image_name = source[len('![]('):-1]
                    self._copy_image(image_name)

                    source_out = (
                        '![]('                   +
                        '{{ site.url }}/images/' +
                        image_name               +
                        ')'
                    )
                    cell['source'] = source_out
