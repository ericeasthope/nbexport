#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authored by Eric Easthope
"""

from parser import Parser

# Initialize notebook interpreter
parser = Parser()

# Get notebooks in directory
parser.get_notebooks()

# Markdown and LaTeX post-processing
# Add JavaScipt tags
# Replace images with Liquid tags
parser.format_math()
parser.format_javascript()
parser.format_image_links()

#
parser.nb2md(include_front_matter=True)

"""
path = '_jupyter/test.ipynb'
from IPython.display import HTML, Markdown
md_raw = !jupyter nbconvert --to markdown {path} --stdout # --template=jekyll.tpl
md_raw = md_raw[1:]
md = '\n'.join(md_raw)
display(Markdown(md))
"""
