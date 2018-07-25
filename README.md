# nbparse
Jupyter notebook parsing and Markdown conversion

### Usage

```python
from nbparse import getNotebooks, nb2md
for notebook in getNotebooks().items():
    nb2md(*notebook)
```
