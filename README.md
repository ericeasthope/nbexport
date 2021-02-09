# nbexport
Personal [`nbconvert`](https://github.com/jupyter/nbconvert)-based exporters for Jupyter notebooks

### Conversion maps

- `.ipynb` to `.html` (custom templates)
- `.ipynb` to `.md` (unstable)
- `.py` to `.ipynb` (incomplete)
- `.py` (to `.ipynb`) to `.md` (incomplete)

### How to use

#### `.ipynb` to `.html`

...

#### Convert `.ipynb` to `.md`

...

In the `nb2md/` directory,

```python
from nbparse import get_notebooks, nb2md
for notebook in get_notebooks().items():
    nb2md(*notebook)
```

```python
from nbparse.parser import Parser
parser = Parser()
parser.get_notebooks()
parser.nb2md(include_front_matter=True)
```


The `Parser` object expects that all notebooks begin with a Markdown cell containing a comment of hash tags, as well as a title using Header 1.

That is, begin every notebook with something like:

```
[//]: # (#math #new)

# A Title
```

The `Parser` object will generate YAML front matter for each notebook using its tags and title:

```yaml
---
layout: post
title: A Title
tags:
  - math
  - new
...
---
```

#### Convert `.py` to `.ipynb`

`null`

#### Convert `.py` (to `.ipynb`) to `.md`

`null`

Useful links:

- [`.ipynb` to Jekyll script](https://gist.github.com/ewjoachim/570022bb7a08403cbe525fe82bd6d3e4)
- [Another `.ipynb` to Jekyll script](https://gist.github.com/jessstringham/1ff8ec24dafc0fcff15d4a0e88be074e)

---

Authored by Eric Easthope

MIT License

Copyright (c) 2020
