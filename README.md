# nbexport
Personal nbconvert exporters for Jupyter notebooks

### Usage

Within `nb2md`:

```python
from nbparse import get_notebooks, nb2md
for notebook in get_notebooks().items():
    nb2md(*notebook)
```
