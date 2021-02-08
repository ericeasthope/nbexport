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

#### Convert `.py` to `.ipynb`

`null`

#### Convert `.py` (to `.ipynb`) to `.md`

`null`

---

Authored by Eric Easthope

MIT License

Copyright (c) 2020
