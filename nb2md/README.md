# nbparse
Jupyter notebook parsing and Markdown conversion

### Usage

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
