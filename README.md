# xmarshal

A Python XML parser that uses existing schema to create Python objects from XML data.

## Distributing

In order to upload `xmarshal` to PyPI, you must first have Cython installed. To generate a source distribution, run:

```bash
$ python setup.py sdist
```

Then, use `twine` to upload it to PyPI. The `pyproject.toml` file will take care of Cython being a build dependency.

```bash
$ twine upload dist/*
```