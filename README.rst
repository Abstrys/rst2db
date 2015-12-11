#########
rst2db.py
#########

A number of tools for reStructuredText (reST) and Sphinx, including:

* A reST to DocBook converter (rst2db) with an included Sphinx builder
  (abstrys.spinx_ext.docbook_builder).

* A reST to Markdown converter (rst2md) with an included Sphinx builder
  (abstrys.sphinx_ext.markdown_builder).


Using the command-line utilities
================================

::

  rst2db <filename> [-e root_element] [-o output_file] [-t template_file]

  rst2md <filename> [-o output_file]

Only the filename to process is required. All other settings are optional.

**Settings:**

 -e root_element  set the root element of the resulting docbook file. If this is
                  not specified, then 'section' will be used.

 -o output_file  set the output filename to write. If this is not specified,
                 then output will be sent to stdout.

 -t template_file  set a template file to use to dress the output. You must have
                   Jinja2 installed to use this feature.

                   Use {{data.root_element}} and {{data.contents}} to represent
                   the output of this script in your template.


Using the Sphinx builders
=========================

Docbook output
--------------

To build DocBook output with Sphinx, add `abstrys.sphinx_ext.docbook_builder` to the *extensions*
list in ``conf.py``::

 extensions = [
    ... other extensions here ...
    abstrys.sphinx_ext.docbook_builder
    ]

There are two configurable parameters for ``conf.py`` that correspond to
``rst2db.py`` parameters:


:docbook_template_file: template file that will be used to position the document
                        parts. Requires Jinja2 to be installed if specified.

:docbook_default_root_element: default root element for a file-level document.
                               Default is 'section'.

Then, build your project using ``sphinx-build`` with the ``-b docbook`` option::

    sphinx-build source output -b docbook


Markdown output
---------------

To build Markdown output with Sphinx, add `abstrys.sphinx_ext.docbook_builder` to the *extensions*
list in ``conf.py``::

 extensions = [
    ... other extensions here ...
    abstrys.sphinx_ext.markdown_builder
    ]

There aren't any configurable options yet. Just build your project with ``-b markdown`` as the
output type::

    sphinx-build source output -b markdown


License
-------

This software is provided under the `BSD 3-Clause`__ license. See the
`LICENSE`__ file for more details.

.. __: http://opensource.org/licenses/BSD-3-Clause
.. __: https://github.com/Abstrys/abstrys-toolkit/blob/master/LICENSE

For more information
--------------------

Contact: Eron Hennessey <eron@abstrys.com>

