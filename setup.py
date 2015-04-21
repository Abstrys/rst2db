#!/usr/bin/env python
from setuptools import setup, find_packages

long_desc = """
Usage
-----

::

  rst2db <filename> [-e root_element] [-o output_file] [-t template_file]

Only the filename to process is required. All other settings are optional.

Settings:

  -e root_element  set the root element of the resulting docbook file. If this
                   is not specified, then 'section' will be used.

  -o output_file  set the output filename to write. If this is not specified,
                  then output will be sent to stdout.

  -t template_file  set a template file to use to dress the output. You must
                    have Jinja2 installed to use this feature.

                    Use {{data.root_element}} and {{data.contents}} to
                    represent the output of this script in your template.
"""

setup(name='rst2db',
      description="""
        A reStructuredText to DocBook converter using Python's docutils.""",
      version='1.0',
      install_requires=['docutils>=0.12', 'lxml>=2.3'],
      packages=find_packages(),
      entry_points={
          'console_scripts': [ 'rst2db = abstrys.cmd_rst2db:run' ],
          },
      author='Eron Hennessey',
      author_email='eron@abstrys.com',
      url='https://github.com/Abstrys/rst2db',
      )
