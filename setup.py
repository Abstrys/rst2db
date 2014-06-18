#!/usr/bin/env python
from distutils.core import setup

long_desc = open('README.rst').read()

setup(name='rst2db',
      description="""
        A reStructuredText to DocBook converter using Python's docutils.""",
      version='0.9',
      requires=['docutils'],
      packages=['abstrys'],
      scripts=['rst2db.py'],
      author='Eron Hennessey',
      author_email='eron@abstrys.com',
      url='https://github.com/Abstrys/rst2db',
      )
