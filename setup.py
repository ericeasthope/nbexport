
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

def main():
    setup(
        name='nbparse',
        version='0.0.dev0',
        author='Eric Easthope',
        license='MIT',
        packages=find_packages(),
        include_package_data=True,
        install_requires=[],
        py_modules=['nbparse']
    )

if __name__ == '__main__':
    main()
