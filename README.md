# nbparse
Jupyter notebook parsing and Markdown conversion

### Usage

```python
from nbparse import get_notebooks, nb2md
for notebook in get_notebooks().items():
    nb2md(*notebook)
```
